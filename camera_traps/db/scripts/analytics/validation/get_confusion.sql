WITH unique_predictions AS (
    SELECT DISTINCT
        video_input_id,
        tracker_id,
        label AS predicted_label
    FROM video_outputs
)

SELECT
    COALESCE(up.predicted_label, 'Missed') AS predicted_label,
    vv.label AS validated_label,
    COUNT(vv.id) AS total
FROM video_validations AS vv
JOIN video_inputs AS vi ON vv.video_input_id = vi.id
LEFT JOIN unique_predictions up
    ON vv.video_input_id = up.video_input_id AND vv.tracker_id = up.tracker_id
WHERE TRUE
    AND CAST(vi.created_at AS DATE) BETWEEN :start_date AND :end_date
    AND EXTRACT(HOUR FROM vi.created_at) >= :start_hour
    AND EXTRACT(HOUR FROM vi.created_at) < :end_hour
    AND (:sites IS NULL OR vi.site = ANY(:sites))
    AND (:species IS NULL OR vv.label = ANY(:species))
GROUP BY 1, 2