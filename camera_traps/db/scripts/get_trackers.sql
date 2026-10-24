SELECT DISTINCT video_input_id, tracker_id, label
FROM video_outputs
WHERE TRUE
    AND video_input_id = :video_id
ORDER BY tracker_id