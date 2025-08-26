import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../../contexts/AuthContext";
import submission from "../../../utils/submission";
import { Edit, Trash, SearchIcon } from "lucide-react";

const CLOUDINARY_BASE_URL = "https://res.cloudinary.com/drm1mr9va/";

const EmployeeList = ({ handleEditEmployee, handleDeleteEmployee }) => {
  const { tokens } = useAuth();
  const [employees, setEmployees] = useState([]);
  const [searchQuery, setSearchQuery] = useState(""); // State for search query
  const navigate = useNavigate();

  useEffect(() => {
    if (!tokens || !tokens.access) {
      navigate("/employee-management");
    }
  }, [tokens, navigate]);

  const loadEmployees = useCallback(async () => {
    if (!tokens?.access) return;
    try {
      const response = await submission("app/management_employee/", "get", null, {
        Authorization: `Bearer ${tokens.access}`,
      });
      setEmployees(response);
    } catch (error) {
      console.error("Error loading employees:", error);
    }
  }, [tokens?.access]);

  useEffect(() => {
    loadEmployees();
  }, [loadEmployees]);

  const handleDeleteEmployeeInternal = async (employeeId) => {
    try {
      await submission(`app/management_employee/${employeeId}`, "delete", null, {
        Authorization: `Bearer ${tokens.access}`,
      });
      setEmployees(employees.filter((emp) => emp.id !== employeeId));
    } catch (error) {
      console.error("Error deleting employee:", error);
    }
  };

  // Logic for filtering employees based on search query
  const filteredEmployees = employees.filter((employee) =>
    `${employee.employee_name} ${employee.role} ${employee.email} ${employee.phone}`
      .toLowerCase()
      .includes(searchQuery.toLowerCase())
  );

  return (
    <div className="bg-white shadow rounded-lg p-4">
      <h2 className="text-lg font-semibold">Employee List</h2>
      <div className="flex items-center p-4">
        <SearchIcon className="w-5 h-5 text-gray-500 mr-2" />
        <input
          type="text"
          placeholder="Search..."
          className="p-2 bg-gray-100 rounded-md focus:outline-none"
          value={searchQuery} // Bind input value to searchQuery state
          onChange={(e) => setSearchQuery(e.target.value)} // Update searchQuery state on input change
        />
      </div>
      <table className="w-full table-auto mt-4 border-collapse border-spacing-0">
  <thead>
    <tr>
      <th className="border p-2">Image</th>
      <th className="border p-2">Name</th>
      <th className="border p-2">Role</th>
      <th className="border p-2">Email</th>
      <th className="border p-2">Phone</th>
      <th className="border p-2">Salary</th>
      <th className="border p-2">Start Date</th>
      <th className="border p-2">Actions</th>
    </tr>
  </thead>
  <tbody>
    {filteredEmployees.map((employee) => (
      <tr key={employee.id} className="text-center">
        <td className="border p-2">
          <div className="w-16 h-16 flex justify-center items-center">
            <img
              src={`${CLOUDINARY_BASE_URL}${employee.image}`}
              alt={employee.employee_name}
              className="w-full h-full object-cover rounded-md"
            />
          </div>
        </td>
        <td className="border p-2"> {employee.employee_name} </td>
        <td className="border p-2"> {employee.role} </td>
        <td className="border p-2"> {employee.email} </td>
        <td className="border p-2"> 0{employee.phone} </td>
        <td className="border p-2"> {employee.salary} </td>
        <td className="border p-2"> {employee.start_date} </td>
        <td className="border p-2">
          <div className="flex justify-center items-center space-x-2">
            <button
              onClick={() => handleEditEmployee(employee)}
              className="bg-blue-500 text-white p-2 rounded-md"
            >
              <Edit className="w-5 h-5" />
            </button>
            <button
              onClick={() => handleDeleteEmployeeInternal(employee.id)}
              className="bg-red-500 text-white p-2 rounded-md"
            >
              <Trash className="w-5 h-5" />
            </button>
          </div>
        </td>
      </tr>
    ))}
  </tbody>
</table>
    </div>
  );
};

export default EmployeeList;