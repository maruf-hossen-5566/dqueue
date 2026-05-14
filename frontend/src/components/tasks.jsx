import Pagination from "@/components/pagination.jsx";
import {deleteJob} from "@/api/jobs.js";
import ResultPopup from "./result_popup";
import ErrorPopup from "./error_popup";
import {useState} from "react";

const Tasks = ({data, setData, setCurrentPage, setErrors}) => {
    const [isLoading, setIsLoading] = useState(false)

    const deleteTask = async (e, id) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            await deleteJob(id);
            setData((prev) => ({
                ...prev,
                items: prev.items.filter((item) => item.id !== id),
            }));
        } catch (error) {
            setErrors((prev) => ([
                JSON.stringify(error?.response?.data?.detail),
                ...prev,
            ]));
        } finally {
            setIsLoading(false);
        }
    };

    const otherResultPopups = document.querySelectorAll(
        'div[id^="result-popup-"]',
    );
    const otherErrorPopups = document.querySelectorAll(
        'div[id^="error-popup-"]',
    );

    const showResultPopup = (id) => {
        const otherPopups = [...otherResultPopups, ...otherErrorPopups].filter(
            (d) => d.id !== `result-popup-${id}`,
        );
        otherPopups.forEach((i) => i.classList.remove("block!"));

        const comp = document.querySelector(`#result-popup-${id}`);
        comp && comp.classList.toggle("block!");
    };

    const showErrorPopup = (id) => {
        const otherPopups = [...otherResultPopups, ...otherErrorPopups].filter(
            (d) => d.id !== `error-popup-${id}`,
        );
        otherPopups.forEach((i) => i.classList.remove("block!"));

        const comp = document.querySelector(`#error-popup-${id}`);
        comp && comp.classList.toggle("block!");
    };

    return (
        <div
            id="tasks-container"
            className="w-full mb-12 mx-auto space-y-6"
        >
            <div className="w-full overflow-auto">
                <table
                    id="tasks-table"
                    className="table-auto w-full mx-auto border border-collapse"
                >
                    <thead className="bg-zinc-100">
                    <tr>
                        <th className="p-6 text-nowrap text-start border-b">
                            ID
                        </th>
                        <th className="p-6 text-nowrap text-start border-b">
                            Task Name
                        </th>
                        <th className="p-6 text-nowrap text-start border-b">
                            Status
                        </th>
                        <th className="p-6 text-nowrap text-start border-b">
                            Created
                        </th>
                        <th className="p-6 text-nowrap text-start border-b ">
                            Result (If Any)
                        </th>
                        <th className="p-6 text-nowrap text-start border-b text-red-500">
                            Error (If Any)
                        </th>
                        <th className="p-6 text-nowrap text-start border-b">
                            Action
                        </th>
                    </tr>
                    </thead>
                    <tbody id="tasks-table-body">
                    {data && data?.items?.length > 0 ? (
                        data?.items?.map((task) => (
                            <tr
                                className="border-b"
                                key={task.id}
                            >
                                <td className="p-6 text-nowrap">
                                    {task.id}
                                </td>
                                <td className="p-6 text-nowrap">
                                    {task.name}
                                </td>
                                <td
                                    className={`p-6 text-nowrap capitalize space-x-1 ${task.status === "pending" ? "text-yellow-500" : task.status === "running" ? "text-blue-500" : task.status === "succeed" ? "text-green-500" : task.status === "failed" && "text-red-500"}`}
                                >
                                    {task.status === "pending" ? (
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
                                            className="inline lucide lucide-circle-dot-dashed-icon lucide-circle-dot-dashed"
                                        >
                                            <path d="M10.1 2.18a9.93 9.93 0 0 1 3.8 0"/>
                                            <path d="M17.6 3.71a9.95 9.95 0 0 1 2.69 2.7"/>
                                            <path d="M21.82 10.1a9.93 9.93 0 0 1 0 3.8"/>
                                            <path d="M20.29 17.6a9.95 9.95 0 0 1-2.7 2.69"/>
                                            <path d="M13.9 21.82a9.94 9.94 0 0 1-3.8 0"/>
                                            <path d="M6.4 20.29a9.95 9.95 0 0 1-2.69-2.7"/>
                                            <path d="M2.18 13.9a9.93 9.93 0 0 1 0-3.8"/>
                                            <path d="M3.71 6.4a9.95 9.95 0 0 1 2.7-2.69"/>
                                            <circle
                                                cx="12"
                                                cy="12"
                                                r="1"
                                            />
                                        </svg>
                                    ) : task.status === "running" ? (
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
                                            className="animate-spin inline lucide lucide-loader-icon lucide-loader"
                                        >
                                            <path d="M12 2v4"/>
                                            <path d="m16.2 7.8 2.9-2.9"/>
                                            <path d="M18 12h4"/>
                                            <path d="m16.2 16.2 2.9 2.9"/>
                                            <path d="M12 18v4"/>
                                            <path d="m4.9 19.1 2.9-2.9"/>
                                            <path d="M2 12h4"/>
                                            <path d="m4.9 4.9 2.9 2.9"/>
                                        </svg>
                                    ) : task.status === "succeed" ? (
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
                                            className="inline lucide lucide-circle-check-icon lucide-circle-check"
                                        >
                                            <circle
                                                cx="12"
                                                cy="12"
                                                r="10"
                                            />
                                            <path d="m9 12 2 2 4-4"/>
                                        </svg>
                                    ) : (
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
                                            className="inline lucide lucide-circle-x-icon lucide-circle-x"
                                        >
                                            <circle
                                                cx="12"
                                                cy="12"
                                                r="10"
                                            />
                                            <path d="m15 9-6 6"/>
                                            <path d="m9 9 6 6"/>
                                        </svg>
                                    )}
                                    <span>{task.status}</span>
                                </td>
                                <td className="p-6 text-nowrap">
                                    {new Date(
                                        task.created_at,
                                    ).toLocaleString()}
                                </td>
                                <td className="p-6 relative">
                                    {task.result && (
                                        <>
                                            <button
                                                onClick={() =>
                                                    showResultPopup(task.id)
                                                }
                                                className="text-blue-500 hover:bg-accent p-2 cursor-pointer border flex gap-1 items-center shrink-0"
                                            >
                                                    <span className="text-nowrap pointer-events-none">
                                                        See result
                                                    </span>
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    width="20"
                                                    height="20"
                                                    viewBox="0 0 24 24"
                                                    fill="none"
                                                    stroke="currentColor"
                                                    strokeWidth="1.5"
                                                    strokeLinecap="round"
                                                    strokeLinejoin="round"
                                                    className="lucide lucide-chevron-down-icon lucide-chevron-down pointer-events-none"
                                                >
                                                    <path d="m6 9 6 6 6-6"/>
                                                </svg>
                                            </button>
                                            <ResultPopup
                                                id={`result-popup-${task.id}`}
                                                task_name={task.name}
                                                result={task.result}
                                            />
                                        </>
                                    )}
                                </td>
                                <td className="p-6 relative">
                                    {task.error && (
                                        <>
                                            <button
                                                onClick={() =>
                                                    showErrorPopup(task.id)
                                                }
                                                className="text-red-500 hover:bg-accent p-2 cursor-pointer border flex gap-1 items-center shrink-0"
                                            >
                                                    <span className="text-nowrap pointer-events-none">
                                                        See error
                                                    </span>
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    width="20"
                                                    height="20"
                                                    viewBox="0 0 24 24"
                                                    fill="none"
                                                    stroke="currentColor"
                                                    strokeWidth="1.5"
                                                    strokeLinecap="round"
                                                    strokeLinejoin="round"
                                                    className="lucide lucide-chevron-down-icon lucide-chevron-down pointer-events-none"
                                                >
                                                    <path d="m6 9 6 6 6-6"/>
                                                </svg>
                                            </button>
                                            <ErrorPopup
                                                id={`error-popup-${task.id}`}
                                                error={task?.error}
                                            />
                                        </>
                                    )}
                                </td>
                                <td className="p-6 text-nowrap sticky bg-white">
                                    <button
                                        onClick={(e) =>
                                            deleteTask(e, task.id)
                                        }
                                        className="size-10 flex items-center justify-center text-red-500 hover:text-white hover:bg-red-500 disabled:opacity-50"
                                        disabled={isLoading}
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
                                            className="lucide lucide-trash-icon lucide-trash"
                                        >
                                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/>
                                            <path d="M3 6h18"/>
                                            <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                                        </svg>
                                    </button>
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr className="border-b">
                            <td className="p-6 text-nowrap">
                                No tasks found
                            </td>
                        </tr>
                    )}
                    </tbody>
                </table>
            </div>

            {/* Pagination */}
            <Pagination
                data={data}
                setCurrentPage={setCurrentPage}
            />
        </div>
    );
};

export default Tasks;
