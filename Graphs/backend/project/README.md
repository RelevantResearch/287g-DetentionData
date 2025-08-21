# 287g Database Frontend

A React frontend application for browsing and filtering 287g database records with an intuitive dashboard interface.

## Features

- **Interactive Dashboard**: Clean, responsive interface with filtering capabilities
- **Dynamic Filtering**: State/County/Status dropdowns with real-time agency table updates
- **Responsive Design**: Optimized for desktop, tablet, and mobile viewing
- **Error Handling**: Comprehensive error states and loading indicators
- **TypeScript**: Full type safety throughout the application

## Tech Stack

- React 18 with TypeScript
- Tailwind CSS for styling
- Vite for build tooling
- Lucide React for icons

## Getting Started

### Prerequisites

- Node.js 16 or higher
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure your API endpoint:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set `REACT_APP_API_URL` to your backend API URL.

4. Start the development server:
   ```bash
   npm run dev
   ```

### API Requirements

The application expects the following API endpoints:

- `GET /api/states` - Returns array of states
- `GET /api/counties?state_id={id}` - Returns counties, optionally filtered by state
- `GET /api/status` - Returns array of status options  
- `GET /api/agencies?state_id={id}&county_id={id}&status_id={id}` - Returns agencies with optional filters

### Expected Data Structures

```typescript
interface State {
  id: number;
  name: string;
}

interface County {
  id: number;
  name: string;
  state_id: number;
}

interface Status {
  id: number;
  name: string;
}

interface Agency {
  id: number;
  name: string;
  type: string;
  support_type: string;
  signed: string;
  last_seen: string;
  status: string;
  county: string;
  state: string;
  extracted_link: string;
}
```

## Build for Production

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── StateDropdown.tsx
│   ├── CountyDropdown.tsx
│   ├── StatusDropdown.tsx
│   ├── AgencyTable.tsx
│   └── LoadingSpinner.tsx
├── hooks/               # Custom React hooks
│   └── useApi.ts
├── services/            # API service layer
│   └── api.ts
├── types/              # TypeScript type definitions
│   └── index.ts
├── App.tsx             # Main application component
└── main.tsx           # Application entry point
```