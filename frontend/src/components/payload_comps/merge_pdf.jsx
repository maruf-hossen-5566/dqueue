const MergePdf = ({handleFormChange}) => {
    return (
        <>
            <label htmlFor="task_payload">Payload</label>
            <input
                type="file"
                accept=".pdf"
                className="p-4 border"
                name="payload"
                id="task_payload"
                onChange={(e) => handleFormChange(e)}
                required
                multiple
            />
        </>
    );
};

export default MergePdf;