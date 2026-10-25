SELECT
    tracker_id,
    MODE() WITHIN GROUP (ORDER BY label) AS label,
    MODE() WITHIN GROUP (ORDER BY label) AS original_label
FROM video_outputs
WHERE video_input_id = :video_id
GROUP BY tracker_id
ORDER BY tracker_id;