WITH churn_por_usuario AS (
  SELECT
    events.user_pseudo_id AS id_usuario,
    COUNTIF(events.event_name IN UNNEST(["page_view", "session_start"])) AS total_interacoes,
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` events
  WHERE PARSE_DATE("%Y%m%d", events.event_date) BETWEEN "2021-01-01" AND "2021-02-01"
  GROUP BY events.user_pseudo_id
),
interacoes_por_quinzena AS (
  SELECT
    events.user_pseudo_id AS id_usuario,
    COUNT(events.event_name) AS total_interacoes,
    COUNTIF(
      PARSE_DATE("%Y%m%d", events.event_date) BETWEEN DATE("2020-12-31") - INTERVAL 14 DAY AND DATE("2020-12-31") - INTERVAL 0 DAY
    ) AS total_interacoes_quinzena_4,
    COUNTIF(
      PARSE_DATE("%Y%m%d", events.event_date) BETWEEN DATE("2020-12-31") - INTERVAL 29 DAY AND DATE("2020-12-31") - INTERVAL 15 DAY
      ) AS total_interacoes_quinzena_3, 
    COUNTIF(
      PARSE_DATE("%Y%m%d", events.event_date) BETWEEN DATE("2020-12-31") - INTERVAL 44 DAY AND DATE("2020-12-31") - INTERVAL 30 DAY
      ) AS total_interacoes_quinzena_2, 
    COUNTIF(
      PARSE_DATE("%Y%m%d", events.event_date) BETWEEN DATE("2020-12-31") - INTERVAL 59 DAY AND DATE("2020-12-31") - INTERVAL 45 DAY
      ) AS total_interacoes_quinzena_1, 
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` events
  WHERE PARSE_DATE("%Y%m%d", events.event_date) BETWEEN DATE("2020-12-31") - INTERVAL 59 DAY AND DATE("2020-12-31") - INTERVAL 0 DAY
  AND events.event_name IN UNNEST(["page_view", "session_start"])
  GROUP BY events.user_pseudo_id
)
SELECT 
  events.user_pseudo_id AS id_usuario,
  COUNT(events.user_pseudo_id) AS total_pedidos,
  ROUND(SUM(events.ecommerce.purchase_revenue_in_usd), 2) AS receita_total_em_usd,
  ROUND(SUM(events.ecommerce.purchase_revenue_in_usd) / COUNT(events.user_pseudo_id), 2) AS ticket_medio_em_usd,
  PARSE_DATE("%Y%m%d", MIN(events.event_date)) AS data_primeiro_pedido,
  PARSE_DATE("%Y%m%d", MAX(events.event_date)) AS data_ultimo_pedido,
  DATE_DIFF(DATE("2021-01-01"), PARSE_DATE("%Y%m%d", MAX(events.event_date)), DAY) AS recencia_dias,
  DATE_DIFF(DATE("2021-01-01"), PARSE_DATE("%Y%m%d", MIN(events.event_date)), DAY) AS dias_desde_primeiro_pedido,
  DATE_DIFF(PARSE_DATE("%Y%m%d", MAX(events.event_date)), PARSE_DATE("%Y%m%d", MIN(events.event_date)), DAY) AS tempo_relacionamento_dias,
  IFNULL(MAX(interacoes_por_quinzena.total_interacoes_quinzena_1), 0) AS total_interacoes_quinzena_1,
  IFNULL(MAX(interacoes_por_quinzena.total_interacoes_quinzena_2), 0) AS total_interacoes_quinzena_2,
  IFNULL(MAX(interacoes_por_quinzena.total_interacoes_quinzena_3), 0) AS total_interacoes_quinzena_3,
  IFNULL(MAX(interacoes_por_quinzena.total_interacoes_quinzena_4), 0) AS total_interacoes_quinzena_4,
  CASE 
    WHEN MAX(churn_por_usuario.total_interacoes) IS NULL
    THEN 1
    ELSE 0
    END
    AS churn
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` events
LEFT JOIN churn_por_usuario ON churn_por_usuario.id_usuario = events.user_pseudo_id
LEFT JOIN interacoes_por_quinzena ON interacoes_por_quinzena.id_usuario = events.user_pseudo_id
WHERE events.event_name = "purchase"
AND PARSE_DATE("%Y%m%d", events.event_date) <= "2020-12-31"
GROUP BY events.user_pseudo_id
ORDER BY tempo_relacionamento_dias DESC;