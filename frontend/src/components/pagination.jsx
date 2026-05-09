const Pagination = ({data, setCurrentPage}) => {
    return (
        <div className="w-full my-6 mx-auto pointer-events-none">
            <div className=" w-full flex justify-between mx-auto">
                <button
                    className="px-6 py-4 pl-3.5 flex items-center gap-1 border cursor-pointer disabled:opacity-30 pointer-events-auto"
                    onClick={() => setCurrentPage(data.page - 1)}
                    disabled={data.page <= 1}
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
                        className="lucide lucide-chevron-left-icon lucide-chevron-left"
                    >
                        <path d="m15 18-6-6 6-6"/>
                    </svg>
                    <span>Previous</span>
                </button>
                <div className="mx-auto px-4 my-auto">
                    <p>Page {data.page} of {data.pages}</p>
                </div>
                <button
                    className="px-6 py-4 pr-3.5 flex items-center gap-1 border cursor-pointer pointer-events-auto disabled:opacity-30"
                    onClick={() => setCurrentPage(data.page + 1)}
                    disabled={data.page >= data.pages}
                >
                    <span>Next</span>
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
                        className="lucide lucide-chevron-right-icon lucide-chevron-right"
                    >
                        <path d="m9 18 6-6-6-6"/>
                    </svg>
                </button>
            </div>
        </div>
    );
};

export default Pagination;