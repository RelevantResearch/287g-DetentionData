import axios from 'axios';

// Optional: set your base URL in .env file
const API_URL = process.env.REACT_APP_API_URL;

export interface State {
  state_id: number;
  state_name: string;
}

export const getStates = async (): Promise<State[]> => {
  const response = await axios.get<State[]>(`${API_URL}/api/states`);
  return response.data;
};
