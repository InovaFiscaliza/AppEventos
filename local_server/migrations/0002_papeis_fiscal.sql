-- Migração 0002: papéis permitidos no cadastro de fiscais (tela Cadastro de Usuários).
-- Decisões:
--   * Papéis globais em TB_FISCAL, a pedido do usuário; diverge de F01/F02 da reunião
--     (papéis só por evento em TB_EVENTO_FISCAL), que continua válido para o vínculo.
--   * Teste e etiquetagem não entra nos papéis permitidos, conforme a tela.
--   * Popula TB_UNIDADE_EXECUTANTE com as Gerências Regionais e Unidades Operacionais.

BEGIN;

ALTER TABLE TB_FISCAL
    ADD COLUMN IF NOT EXISTS IC_COORDENACAO SMALLINT NOT NULL
        CONSTRAINT DF_TB_FISCAL_IC_COORDENACAO_01 DEFAULT 0
        CONSTRAINT CC_TB_FISCAL_IC_COORDENACAO_01 CHECK (IC_COORDENACAO IN (0, 1)),
    ADD COLUMN IF NOT EXISTS IC_ABORDAGEM SMALLINT NOT NULL
        CONSTRAINT DF_TB_FISCAL_IC_ABORDAGEM_01 DEFAULT 0
        CONSTRAINT CC_TB_FISCAL_IC_ABORDAGEM_01 CHECK (IC_ABORDAGEM IN (0, 1)),
    ADD COLUMN IF NOT EXISTS IC_MONITORACAO SMALLINT NOT NULL
        CONSTRAINT DF_TB_FISCAL_IC_MONITORACAO_01 DEFAULT 0
        CONSTRAINT CC_TB_FISCAL_IC_MONITORACAO_01 CHECK (IC_MONITORACAO IN (0, 1));

INSERT INTO TB_UNIDADE_EXECUTANTE (SG_UNIDADE_EXECUTANTE, NO_UNIDADE_EXECUTANTE) VALUES
    ('GR01', 'Gerência Regional no Estado de São Paulo'),
    ('GR02', 'Gerência Regional nos Estados do Rio de Janeiro e Espírito Santo'),
    ('GR03', 'Gerência Regional nos Estados do Paraná e Santa Catarina'),
    ('GR04', 'Gerência Regional no Estado de Minas Gerais'),
    ('GR05', 'Gerência Regional no Estado do Rio Grande do Sul'),
    ('GR06', 'Gerência Regional nos Estados de Pernambuco, Paraíba e Alagoas'),
    ('GR07', 'Gerência Regional nos Estados de Goiás, Mato Grosso, Mato Grosso do Sul e Tocantins'),
    ('GR08', 'Gerência Regional nos Estados da Bahia e Sergipe'),
    ('GR09', 'Gerência Regional nos Estados do Ceará, Rio Grande do Norte e Piauí'),
    ('GR10', 'Gerência Regional nos Estados do Pará, Maranhão e Amapá'),
    ('GR11', 'Gerência Regional nos Estados do Amazonas, Acre, Rondônia e Roraima'),
    ('UO00.1', 'Unidade Operacional do Distrito Federal'),
    ('UO02.1', 'Unidade Operacional no Estado do Espírito Santo'),
    ('UO03.1', 'Unidade Operacional no Estado de Santa Catarina'),
    ('UO06.1', 'Unidade Operacional no Estado de Alagoas'),
    ('UO06.2', 'Unidade Operacional no Estado da Paraíba'),
    ('UO07.1', 'Unidade Operacional no Estado de Mato Grosso'),
    ('UO07.2', 'Unidade Operacional no Estado de Mato Grosso do Sul'),
    ('UO07.3', 'Unidade Operacional no Estado de Tocantins'),
    ('UO08.1', 'Unidade Operacional no Estado de Sergipe'),
    ('UO09.1', 'Unidade Operacional no Estado do Rio Grande do Norte'),
    ('UO09.2', 'Unidade Operacional no Estado do Piauí'),
    ('UO10.1', 'Unidade Operacional no Estado do Maranhão'),
    ('UO10.2', 'Unidade Operacional no Estado do Amapá'),
    ('UO11.1', 'Unidade Operacional no Estado de Rondônia'),
    ('UO11.2', 'Unidade Operacional no Estado do Acre'),
    ('UO11.3', 'Unidade Operacional no Estado de Roraima')
ON CONFLICT (SG_UNIDADE_EXECUTANTE) DO UPDATE
    SET NO_UNIDADE_EXECUTANTE = EXCLUDED.NO_UNIDADE_EXECUTANTE
    -- Corrige só nomes provisórios de versões locais desta migração; nomes do servidor ficam.
    WHERE TB_UNIDADE_EXECUTANTE.NO_UNIDADE_EXECUTANTE LIKE '%(provisório)';

COMMENT ON TABLE TB_FISCAL IS 'Cadastro funcional de fiscais e papéis permitidos IC_COORDENACAO, IC_ABORDAGEM e IC_MONITORACAO (0 - Não; 1 - Sim). NO_FISCAL é dado pessoal identificador.';

COMMIT;
