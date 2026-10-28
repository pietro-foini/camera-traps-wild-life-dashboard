SELECT
    vi.id,
    vi.site,
    vi.filename,
    vi.duration,
    vi.created_at
FROM video_inputs AS vi
WHERE TRUE
    AND vi.status = 'COMPLETED'
    AND CAST(vi.created_at AS DATE) BETWEEN :start_date AND :end_date
    AND EXTRACT(HOUR FROM vi.created_at) >= :start_hour
    AND EXTRACT(HOUR FROM vi.created_at) < :end_hour
    AND (:sites IS NULL OR vi.site = ANY(:sites))
    AND EXISTS (
        SELECT 1
        FROM video_outputs AS vo
        WHERE vo.video_input_id = vi.id
            AND (:species IS NULL OR vo.label = ANY(:species))
    )
ORDER BY
    RANDOM()
LIMIT 1;