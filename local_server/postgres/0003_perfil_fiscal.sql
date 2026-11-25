-- Atualiza TB_FISCAL após 0002_ajustes_novobd.sql.
\set ON_ERROR_STOP on

BEGIN;
SET LOCAL search_path TO "SC_EVENTOS";
SET LOCAL lock_timeout = '5s';

ALTER TABLE "TB_FISCAL"
    ADD COLUMN IF NOT EXISTS "NA_FISCAL_EMAIL" VARCHAR(254),
    ADD COLUMN IF NOT EXISTS "NA_JOB_TITLE" TEXT,
    ADD COLUMN IF NOT EXISTS "NA_DEPARTMENT" TEXT,
    ADD COLUMN IF NOT EXISTS "NA_LOCATION" TEXT,
    ADD COLUMN IF NOT EXISTS "NA_URL_PROFILE_IMG" TEXT,
    ADD COLUMN IF NOT EXISTS "DT_CREATED_AT" TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS "DT_UPDATED_AT" TIMESTAMPTZ;

-- Preserva a sigla da unidade como localização nos cadastros anteriores.
DO $migration$
BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_attribute
        WHERE attrelid = '"TB_FISCAL"'::regclass
          AND attname = 'SG_UNIDADE_EXECUTANTE'
          AND NOT attisdropped
    ) THEN
        UPDATE "TB_FISCAL"
        SET "NA_LOCATION" = "SG_UNIDADE_EXECUTANTE"
        WHERE "NA_LOCATION" IS NULL;

        ALTER TABLE "TB_FISCAL" DROP COLUMN "SG_UNIDADE_EXECUTANTE";
    END IF;
END
$migration$;

-- Datas legadas desconhecidas ficam nulas. Atualizações futuras são datadas pela aplicação.
ALTER TABLE "TB_FISCAL"
    ALTER COLUMN "DT_CREATED_AT" SET DEFAULT now(),
    ALTER COLUMN "DT_UPDATED_AT" SET DEFAULT now();

COMMENT ON TABLE "TB_FISCAL" IS
    'Cadastro funcional de fiscais. Nome, e-mail e imagem de perfil podem identificar pessoas.';

COMMIT;
