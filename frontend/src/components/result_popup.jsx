function ResultPopup({id, task_name, result}) {
    return (
        task_name && result &&
        (
            <div
                id={id}
                className="p-6 max-w-sm min-w-sm w-full z-50 absolute top-full -mt-4 right-0 hidden border bg-white shadow space-y-4"
            >
                {(task_name === "image_optimize" || task_name === "merge_pdf" || task_name === "qrcode_generate") ? (
                    result?.map((item) => (
                        <a
                            key={item?.id}
                            href={item?.url}
                            target="_blank"
                            className="text-blue-500 wrap-break-word text-wrap hover:underline line-clamp-1"
                        >
                            {item?.url}
                        </a>
                    ))
                ) : task_name && task_name === "string_process" ? (
                    <code className="wrap-break-word">
                        {JSON.stringify(result)}
                    </code>
                ) : (
                    <></>
                )}
            </div>
        )
    );
}

export default ResultPopup;
