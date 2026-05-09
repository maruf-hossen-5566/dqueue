const SendEmail = ({handleFormChange}) => {
    return (
        <>
            <label htmlFor="task_payload">Payload</label>
            <textarea
                className="p-4 border"
                name="payload"
                id="task_payload"
                placeholder="user1@example.com, user2@exmaple.com, ..."
                onChange={handleFormChange}
                required
            ></textarea>
        </>
    );
};

export default SendEmail;