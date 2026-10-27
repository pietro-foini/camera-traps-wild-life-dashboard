SELECT
  vi.id,
  CAST(vi.created_at AS DATE) AS created_at,
  COUNT(DISTINCT vo.tracker_id) AS total
FROM video_inputs AS vi
LEFT JOIN video_outputs AS vo ON vi.id = vo.video_input_id
WHERE TRUE
  AND CAST(vi.created_at AS DATE) BETWEEN :start_date AND :end_date
  AND EXTRACT(HOUR FROM vi.created_at) >= :start_hour
  AND EXTRACT(HOUR FROM vi.created_at) < :end_hour
  AND (:sites IS NULL OR vi.site = ANY(:sites))
  AND (:species IS NULL OR vo.label = ANY(:species))
GROUP BY 1, 2
ORDER BY 2