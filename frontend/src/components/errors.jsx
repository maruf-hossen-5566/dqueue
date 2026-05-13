const Errors = ({errors, setErrors}) => {

    const deleteErrors = (idx) => {
        setErrors(prev => (prev.filter((_, i) => i !== idx)))
    }

    console.log("Errors", errors)


    return (
        <ul
            className="w-full space-y-4 sticky top-0 z-40"
        >
            {
                errors?.map((error, index) => (
                    error && typeof JSON.parse(error) === "object" ? (
                            <li
                                key={index}
                                className="w-full px-6 py-4 bg-red-500 text-white flex items-center justify-between gap-4 border"
                            >
                                <span>{JSON.parse(error)[0]["loc"].at(1)} - {JSON.parse(error)[0]["msg"]}</span>
                                <button
                                    onClick={() => deleteErrors(index)}
                                    className="size-10 flex items-center justify-center hover:bg-red-700"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="24"
                                        height="24"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        strokeWidth="2"
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        className="lucide lucide-x-icon lucide-x"
                                    >
                                        <path d="M18 6 6 18"/>
                                        <path d="m6 6 12 12"/>
                                    </svg>
                                </button>
                            </li>
                        )
                        :
                        (
                            <li
                                key={index}
                                className="w-full px-6 py-4 bg-red-500 text-white flex items-center justify-between gap-4 border"
                            >
                                <span>{JSON.parse(error)}</span>
                                <button
                                    onClick={() => deleteErrors(index)}
                                    className="size-10 flex items-center justify-center hover:bg-red-700"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="24"
                                        height="24"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        strokeWidth="2"
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        className="lucide lucide-x-icon lucide-x"
                                    >
                                        <path d="M18 6 6 18"/>
                                        <path d="m6 6 12 12"/>
                                    </svg>
                                </button>
                            </li>
                        )
                ))
            }
        </ul>
    );
};

export default Errors;