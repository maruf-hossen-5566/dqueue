import client from "@/api/client.js"

export const getJobs = (data) => {
    return client.get("/jobs/", {
        params: {
            page: data.page,
        }
    });
}

export const createJob = (data) => {
    return client.post("/jobs/", data,);
}

export const deleteJob = (id) => {
    return client.delete(`/jobs/${id}/`);
}