import {useEffect, useState} from "react";
import SendEmail from "@/components/payload_comps/send_email.jsx";
import ImageOptimize from "@/components/payload_comps/image_optimize.jsx";
import {createJob} from "@/api/jobs.js";
import StringProcess from "@/components/payload_comps/string_process.jsx";
import MergePdf from "@/components/payload_comps/merge_pdf.jsx";
import QrcodeGenerate from "@/components/payload_comps/qrcode_generate.jsx";

const CreateTask = ({setData, setErrors}) => {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        name: "merge_pdf",
        max_retries: 3,
        payload: null,
    });

    useEffect(() => {
        setFormData((prevState) => ({
            ...prevState,
            payload: null,
        }));
    }, [formData?.name]);

    const handleFormChange = (e) => {
        const {name, type, files, value} = e.target;

        setFormData((prevState) => ({
            ...prevState,
            [name]: type === "file" ? files : value,
        }));

        console.log("FormData: changed", formData);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        console.log("FOrmData: ", formData);

        const data = new FormData();
        data.set("name", formData.name);
        data.set("max_retries", formData.max_retries);

        if (
            (formData.name === "image_optimize" || formData.name === "merge_pdf") && formData.payload
        )
            Object.values(formData.payload).map((file) => {
                data.append("files", file);
            });
        else {
            formData.payload && data.set("payload", formData.payload);
        }

        try {
            const res = await createJob(data);
            setData((prev) => ({...prev, items: [res.data, ...prev.items]}));
        } catch (error) {
            console.log("Error: ", error?.response);
            setErrors((prev) => [
                JSON.stringify(error?.response?.data?.detail),
                ...prev,
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form
            className="grid w-full grid-cols-2 mt-12 gap-8"
            onSubmit={handleSubmit}
        >
            <div className="flex flex-col gap-2">
                <label htmlFor="task_name">Task name</label>
                <select
                    name="name"
                    id="task_name"
                    className="p-4 border"
                    onChange={(e) => handleFormChange(e)}
                    value={formData.name}
                >
                    <option value="send_email">Send Email</option>
                    <option value="image_optimize">Image Optimize</option>
                    <option value="merge_pdf">Merge PDF</option>
                    <option value="qrcode_generate">QR Code Generate</option>
                    <option value="string_process">String Process</option>
                </select>
            </div>
            <div className="flex flex-col gap-2">
                <label htmlFor="max_retries">Max retry</label>
                <input
                    type="number"
                    name="max_retries"
                    id="max_retries"
                    value={formData.max_retries}
                    onChange={(e) => handleFormChange(e)}
                    className="p-4 border"
                    // max={10}
                    // min={1}
                    // required
                />
            </div>
            <div className="col-span-full flex flex-col gap-2">
                {formData.name === "send_email" ? (
                    <SendEmail handleFormChange={handleFormChange}/>
                ) : (formData.name === "image_optimize") ? (
                    <ImageOptimize handleFormChange={handleFormChange}/>
                ) : formData.name === "merge_pdf" ? (
                    <MergePdf handleFormChange={handleFormChange}></MergePdf>
                ) : formData.name === "qrcode_generate" ? (
                    <QrcodeGenerate handleFormChange={handleFormChange}/>
                ) : formData.name === "string_process" ? (
                    <StringProcess handleFormChange={handleFormChange}/>
                ) : (
                    ""
                )}
            </div>
            <div className="col-span-full flex flex-col gap-2">
                <button
                    type="submit"
                    className="ml-auto w-max p-4 text-white bg-zinc-900 cursor-pointer disabled:opacity-50"
                    disabled={loading}
                >
                    Queue task
                </button>
            </div>
        </form>
    );
};

export default CreateTask;
