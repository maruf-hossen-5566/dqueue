const QrcodeGenerate = ({handleFormChange}) => {
    return (
        <>
            <label htmlFor="task_payload">Payload</label>
            <textarea
                className="p-4 border"
                name="payload"
                id="task_payload"
                placeholder="www.example.com, ..."
                onChange={handleFormChange}
                required
            ></textarea>
        </>
    );
};

export default QrcodeGenerate;