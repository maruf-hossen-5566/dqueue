import {useState} from "react";
import {NavLink} from "react-router-dom";

const Header = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false)

    return (
        <div>
            <div className="w-full py-4 flex items-center justify-between gap-4">
                <h1 className="text-2xl font-bold">DQueue</h1>
                {
                    isAuthenticated ? (
                        <button className="p-4 border flex items-center gap-2 cursor-pointer hover:bg-zinc-900">
                            <span className="max-w-50 text-ellipsis overflow-hidden">smmarufhossen5566@gmail.com</span>
                            <span><svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="1.5"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                className="lucide lucide-chevron-down-icon lucide-chevron-down"
                            ><path d="m6 9 6 6 6-6"/></svg>
                    </span>
                        </button>) : (<div className="flex items-center gap-4">
                        <NavLink
                            to="login"
                            className="p-4 flex items-center gap-2 cursor-pointer hover:bg-accent"
                        >Login</NavLink>
                        <NavLink
                            to="register"
                            className="p-4 border flex items-center gap-2 cursor-pointer hover:bg-accent"
                        >Register</NavLink>
                    </div>)
                }
            </div>
        </div>
    );
};

export default Header;