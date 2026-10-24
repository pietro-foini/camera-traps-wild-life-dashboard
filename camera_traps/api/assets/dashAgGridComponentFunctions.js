var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.DeleteButton = function (params) {
    const isDisabled = params.data.tracker_id !== null && params.data.tracker_id !== undefined;

    function onClick() {
        if (!isDisabled) {
            params.api.applyTransaction({ remove: [params.node.data] });
        }
    }

    return React.createElement(
        "button",
        {
            onClick: onClick,
            disabled: isDisabled,
            style: {
                border: "none",
                background: "transparent",
                cursor: isDisabled ? "not-allowed" : "pointer",
                opacity: isDisabled ? 0.3 : 1,
                color: isDisabled ? "gray" : "red",
                fontWeight: "bold",
                width: "100%",
                height: "100%",
            },
        },
        "✕"
    );
};