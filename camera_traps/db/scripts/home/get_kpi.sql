SELECT
    vi.site,
    COUNT(DISTINCT vi.id) AS total_videos,
    COUNT(DISTINCT (vo.video_input_id, vo.tracker_id)) FILTER (WHERE vo.tracker_id IS NOT NULL) AS total_tracks
FROM video_inputs AS vi
LEFT JOIN video_outputs AS vo
    ON vi.id = vo.video_input_id
WHERE TRUE
    AND CAST(vi.created_at AS DATE) BETWEEN :start_date AND :end_date
    AND EXTRACT(HOUR FROM vi.created_at) >= :start_hour
    AND EXTRACT(HOUR FROM vi.created_at) < :end_hour
    AND (:sites IS NULL OR vi.site = ANY(:sites))
GROUP BY
    vi.site
ORDER BY
    vi.site