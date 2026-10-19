-- ==============================================================================
-- PROYECTO: Sistema OLTP de Evaluación del Nivel de Manejo de Excel (EECA-UCV)
-- ARQUITECTURA: 3FN en PostgreSQL (Supabase Cloud)
-- ==============================================================================

-- 1. CATÁLOGOS BASE (Dimensiones y dominios cerrados)

-- 1.1 Catálogo de Secciones del Propedéutico (Variable 1)
CREATE TABLE IF NOT EXISTS cat_secciones (
    id_seccion SMALLINT PRIMARY KEY,
    nombre_seccion VARCHAR(20) UNIQUE NOT NULL
);

INSERT INTO cat_secciones (id_seccion, nombre_seccion) VALUES
(11, 'Sección 11'),
(12, 'Sección 12')
ON CONFLICT (id_seccion) DO NOTHING;

-- 1.2 Catálogo de Operaciones Básicas en Excel (Variable 6)
CREATE TABLE IF NOT EXISTS cat_operaciones_excel (
    id_operacion SMALLINT PRIMARY KEY,
    nombre_operacion VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO cat_operaciones_excel (id_operacion, nombre_operacion) VALUES
(1, 'Sumar'),
(2, 'Restar'),
(3, 'Multiplicar'),
(4, 'Dividir'),
(5, 'Crear gráficos'),
(6, 'Crear tablas dinámicas')
ON CONFLICT (id_operacion) DO NOTHING;

-- 1.3 Catálogo de Percepción de Utilidad Profesional y Académica (Variable 9)
CREATE TABLE IF NOT EXISTS cat_percepcion_utilidad (
    id_percepcion SMALLINT PRIMARY KEY,
    descripcion_segmento VARCHAR(120) UNIQUE NOT NULL
);

INSERT INTO cat_percepcion_utilidad (id_percepcion, descripcion_segmento) VALUES
(1, 'Puede ayudarle y facilitarle la carrera'),
(2, 'Le será útil para diversos fines generales'),
(3, 'Brindará mejores oportunidades en el ámbito profesional y laboral'),
(4, 'Será útil y brindará oportunidades tanto en la carrera como en el ámbito profesional')
ON CONFLICT (id_percepcion) DO NOTHING;

-- 1.4 Catálogo de Autopercepción del Nivel de Manejo (Variable 10 - Escala Likert Ordinal)
CREATE TABLE IF NOT EXISTS cat_niveles_manejo (
    id_nivel SMALLINT PRIMARY KEY,
    etiqueta_ordinal VARCHAR(20) UNIQUE NOT NULL
);

INSERT INTO cat_niveles_manejo (id_nivel, etiqueta_ordinal) VALUES
(1, 'Muy Malo'),
(2, 'Malo'),
(3, 'Regular'),
(4, 'Bueno'),
(5, 'Muy Bueno')
ON CONFLICT (id_nivel) DO NOTHING;


-- 2. TABLAS TRANSACCIONALES EN TERCERA FORMA NORMAL (3FN)

-- 2.1 Entidad Maestra de Identificación de Estudiantes (Datos Personales)
CREATE TABLE IF NOT EXISTS estudiantes (
    cedula VARCHAR(20) PRIMARY KEY,
    nombre_completo VARCHAR(120) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    id_seccion SMALLINT NOT NULL REFERENCES cat_secciones(id_seccion),
    edad SMALLINT NOT NULL CHECK (edad >= 15 AND edad <= 75),
    genero VARCHAR(15) NOT NULL CHECK (genero IN ('Femenino', 'Masculino')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    CONSTRAINT uq_estudiante_identidad UNIQUE (cedula, correo)
);

-- 2.2 Transacciones de Respuestas de Encuestas (Relación 1:1 estricta por Cédula)
CREATE TABLE IF NOT EXISTS encuestas_estudiantes (
    id_encuesta UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    cedula VARCHAR(20) NOT NULL UNIQUE REFERENCES estudiantes(cedula) ON DELETE CASCADE,
    ha_usado_excel BOOLEAN NOT NULL,
    cantidad_operaciones SMALLINT NOT NULL CHECK (cantidad_operaciones >= 0 AND cantidad_operaciones <= 6),
    interes_electiva BOOLEAN NOT NULL,
    tiene_herramientas BOOLEAN NOT NULL,
    id_percepcion SMALLINT NOT NULL REFERENCES cat_percepcion_utilidad(id_percepcion),
    id_nivel SMALLINT NOT NULL REFERENCES cat_niveles_manejo(id_nivel)
);

-- 2.3 Tabla Puente para Desacoplamiento N:M de Operaciones (3FN)
CREATE TABLE IF NOT EXISTS encuesta_operaciones (
    id_encuesta UUID NOT NULL REFERENCES encuestas_estudiantes(id_encuesta) ON DELETE CASCADE,
    id_operacion SMALLINT NOT NULL REFERENCES cat_operaciones_excel(id_operacion),
    PRIMARY KEY (id_encuesta, id_operacion)
);


-- 3. ÍNDICES DE RENDIMIENTO (Supabase Postgres Best Practices)
CREATE INDEX IF NOT EXISTS idx_estudiantes_seccion ON estudiantes (id_seccion);
CREATE INDEX IF NOT EXISTS idx_encuestas_cedula ON encuestas_estudiantes (cedula);
CREATE INDEX IF NOT EXISTS idx_encuestas_id_percepcion ON encuestas_estudiantes (id_percepcion);
CREATE INDEX IF NOT EXISTS idx_encuestas_id_nivel ON encuestas_estudiantes (id_nivel);
CREATE INDEX IF NOT EXISTS idx_encuesta_operaciones_id_operacion ON encuesta_operaciones (id_operacion);


-- 4. SEGURIDAD A NIVEL DE FILA (Row Level Security - RLS)
ALTER TABLE cat_secciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE cat_operaciones_excel ENABLE ROW LEVEL SECURITY;
ALTER TABLE cat_percepcion_utilidad ENABLE ROW LEVEL SECURITY;
ALTER TABLE cat_niveles_manejo ENABLE ROW LEVEL SECURITY;
ALTER TABLE estudiantes ENABLE ROW LEVEL SECURITY;
ALTER TABLE encuestas_estudiantes ENABLE ROW LEVEL SECURITY;
ALTER TABLE encuesta_operaciones ENABLE ROW LEVEL SECURITY;

-- Políticas de lectura para catálogos
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Permitir lectura publica de secciones') THEN
        CREATE POLICY "Permitir lectura publica de secciones" ON cat_secciones FOR SELECT TO anon, authenticated USING (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Permitir lectura publica de operaciones') THEN
        CREATE POLICY "Permitir lectura publica de operaciones" ON cat_operaciones_excel FOR SELECT TO anon, authenticated USING (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Permitir lectura publica de percepcion utilidad') THEN
        CREATE POLICY "Permitir lectura publica de percepcion utilidad" ON cat_percepcion_utilidad FOR SELECT TO anon, authenticated USING (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Permitir lectura publica de niveles manejo') THEN
        CREATE POLICY "Permitir lectura publica de niveles manejo" ON cat_niveles_manejo FOR SELECT TO anon, authenticated USING (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Permitir insercion y lectura de estudiantes') THEN
        CREATE POLICY "Permitir insercion y lectura de estudiantes" ON estudiantes FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Permitir insercion y lectura de encuestas') THEN
        CREATE POLICY "Permitir insercion y lectura de encuestas" ON encuestas_estudiantes FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Permitir insercion y lectura de encuesta_operaciones') THEN
        CREATE POLICY "Permitir insercion y lectura de encuesta_operaciones" ON encuesta_operaciones FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);
    END IF;
END $$;
