import {useEffect, useState} from "react";
import {getJobs} from "@/api/jobs.js";
import Errors from "@/components/errors.jsx";
import CreateTask from "@/components/create_task.jsx";
import Stats from "@/components/stats.jsx";
import Tasks from "@/components/tasks.jsx";
import Header from "@/components/header.jsx";


function App() {
    const [data, setData] = useState({});
    const [currentPage, setCurrentPage] = useState(data.page || 1);
    const [errors, setErrors] = useState([]);

    useEffect(() => {
        const getTasks = async () => {
            const res = await getJobs({page: currentPage});
            setData(res.data);
        };

        getTasks();
        const intervalId = setInterval(getTasks, 5000);

        return () => clearInterval(intervalId);
    }, [currentPage]);

    return (
        <div className="w-full mb-12 px-6 flex flex-col justify-center">
            <div className="max-w-7xl w-full mx-auto">
                <Header/>
                <Errors
                    errors={errors}
                    setErrors={setErrors}
                />
                <div className="w-full mt-12 space-y-6">
                    <CreateTask
                        setData={setData}
                        setErrors={setErrors}
                    />
                    <hr className="my-12"/>
                    <Stats data={data}/>
                    <Tasks
                        data={data}
                        setCurrentPage={setCurrentPage}
                        setData={setData}
                    />
                </div>
            </div>
        </div>
    );
}

export default App;
