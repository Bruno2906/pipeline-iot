-- View 1: média de temperatura por dispositivo e por local (In/Out)
-- Compara a temperatura média interna vs. externa em cada sala.
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT
    device_id,
    location,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temp,
    COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY device_id, location;

-- View 2: quantidade de leituras por hora do dia
-- Mostra em quais horas os sensores mais registram dados.
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM noted_at)::int AS hora,
    COUNT(*) AS contagem
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM noted_at)
ORDER BY hora;

-- View 3: temperaturas máxima, mínima e média por dia
-- Mostra a variação diária e a amplitude térmica ao longo do período.
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    noted_at::date AS data,
    MAX(temperature) AS temp_max,
    MIN(temperature) AS temp_min,
    ROUND(AVG(temperature)::numeric, 2) AS temp_media
FROM temperature_readings
GROUP BY noted_at::date
ORDER BY data;