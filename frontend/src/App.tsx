// src/App.tsx
import { BrowserRouter, Routes, Route, Navigate, Link } from "react-router-dom";
import ProfilePage from "./pages/ProfilePage";
import ChangePasswordPage from "./pages/ChangePasswordPage";

export default function App() {
  return (
    <BrowserRouter>
      {/* Barra simple de navegación (opcional, puedes quitarla) */}
      <div style={{ padding: "10px 20px", display: "flex", gap: 12 }}>
        <Link to="/perfil" className="btn">Perfil</Link>
        <Link to="/cambiar-clave" className="btn">Cambiar contraseña</Link>
      </div>

      <Routes>
        <Route path="/perfil" element={<ProfilePage />} />
        <Route path="/cambiar-clave" element={<ChangePasswordPage />} />
        <Route path="*" element={<Navigate to="/perfil" />} />
      </Routes>
    </BrowserRouter>
  );
}
