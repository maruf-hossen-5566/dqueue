function ErrorPopup({ id, error }) {
    return (
        <div
            id={id}
            className="p-6 text-red-500 max-w-sm min-w-sm w-full z-50 absolute top-full -mt-4 right-0 hidden border bg-white shadow"
        >
            <p className="w-full wrap-break-word">{String(error)}</p>
        </div>
    );
}

export default ErrorPopup;
