export interface State {
  state_name: ReactNode;
  state_id: Key | null | undefined;
  id: number;
  name: string;
  code?: string;
}

export interface County {
  id: number;
  name: string;
  state_id: number;
  state_name?: string;
}


export interface Status {
  status_id: Key | null | undefined;
  status_name: ReactNode;
  id: number;
  name: string;
  description?: string;
}

export interface Agency {
  agency_name: ReactNode;
  id: number;
  name: string;
  type: string;
  support_type: string;
  signed: string;
  last_seen: string;
  county: { county_id: number; county_name: string };
  state: { state_id: number; state_name: string };
  status: { status_id: number; status_name: string };
  extracted_link: string;
}


export interface ApiFilters {
  state_id?: number;
  county_id?: number;
  status_id?: number;
  status_name?: number;
}