const StringProcess = ({handleFormChange}) => {
    return (
        <>
            <label htmlFor="task_payload">Payload</label>
            <textarea
                className="p-4 border"
                name="payload"
                id="task_payload"
                placeholder="Lorem ipsum dolor sit amet, consectetur adipisicing elit..."
                onChange={handleFormChange}
                required
            ></textarea>
        </>
    );
};

export default StringProcess;