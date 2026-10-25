WITH tracker_lengths AS (
    SELECT
        video_input_id,
        tracker_id,
        COUNT(frame_id) AS num_frames
    FROM video_outputs
    GROUP BY video_input_id, tracker_id
)
SELECT
    vv.label AS species,
    tl.num_frames
FROM video_validations vv
JOIN video_inputs vi ON vv.video_input_id = vi.id
JOIN tracker_lengths tl
    ON vv.video_input_id = tl.video_input_id AND vv.tracker_id = tl.tracker_id
WHERE TRUE
    AND CAST(vi.created_at AS DATE) BETWEEN :start_date AND :end_date
    AND (:sites IS NULL OR vi.site = ANY(:sites))