INSERT INTO video_validations (
    video_input_id,
    tracker_id,
    label,
    comments,
    is_modified,
    validated_by,
    created_at
)
VALUES (
    :video_input_id,
    :tracker_id,
    :label,
    :comments,
    :is_modified,
    :validated_by,
    NOW()
);