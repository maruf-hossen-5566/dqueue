const Stats = ({data}) => {
    return (
        <div className="w-full grid grid-cols-3 lg:grid-cols-6 gap-6 mx-auto">
            <div className="col-span-2 p-6 border space-x-1">
                <span className="text-4xl font-semibold">{data.total}</span>
                <span className="text-lg">Total</span>
            </div>
            <div className="col-span-1 p-6 border space-x-1">
                <span className="text-4xl font-semibold text-blue-500">{data.running_item_count}</span>
                <span className="text-lg">Running</span>
            </div>
            <div className="col-span-1 p-6 border space-x-1">
                <span className="text-4xl font-semibold text-yellow-500">{data.pending_item_count}</span>
                <span className="text-lg">Pending</span>
            </div>
            <div className="col-span-1 p-6 border space-x-1">
                <span className="text-4xl font-semibold text-green-500">{data.succeed_item_count}</span>
                <span className="text-lg">Completed</span>
            </div>
            <div className="col-span-1 p-6 border space-x-1">
                <span className="text-4xl font-semibold text-red-500">{data.failed_item_count}</span>
                <span className="text-lg">Failed</span>
            </div>
        </div>
    );
};

export default Stats;