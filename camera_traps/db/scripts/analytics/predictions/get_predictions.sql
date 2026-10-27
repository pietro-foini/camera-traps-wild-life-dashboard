SELECT
    vo.label AS species,
    COUNT(DISTINCT (vo.video_input_id, vo.tracker_id)) AS total
FROM video_inputs AS vi
JOIN video_outputs AS vo ON vi.id = vo.video_input_id
WHERE TRUE
    AND CAST(vi.created_at AS DATE) BETWEEN :start_date AND :end_date
    AND EXTRACT(HOUR FROM vi.created_at) >= :start_hour
    AND EXTRACT(HOUR FROM vi.created_at) < :end_hour
    AND (:sites IS NULL OR vi.site = ANY(:sites))
    AND (:species IS NULL OR vo.label = ANY(:species))
GROUP BY
    vo.label
ORDER BY
    total