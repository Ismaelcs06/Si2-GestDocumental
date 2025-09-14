import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { api } from "../lib/api";
import type { AxiosError } from "axios";

const ProfileSchema = z.object({
  username: z.string().optional(),
  first_name: z.string().min(1, "Nombre requerido"),
  last_name: z.string().min(1, "Apellido requerido"),
  email: z.string().email("Email inválido"),
  profile: z.object({
    phone: z.string().optional(),
    bio: z.string().max(500, "Máximo 500 caracteres").optional(),
  }),
});
type ProfileFormData = z.infer<typeof ProfileSchema>;

/** Obtiene un mensaje legible desde un error de Axios u otro tipo */
function extractErrorMessage(error: unknown): string {
  const DEFAULT_MSG = "Ocurrió un error. Intenta de nuevo.";
  // Comprobamos si parece un AxiosError
  const ax = error as AxiosError<{ detail?: string }>;
  return ax?.response?.data?.detail ?? DEFAULT_MSG;
}

export default function ProfilePage() {
  const [loading, setLoading] = useState(true);
  const [saveMsg, setSaveMsg] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } =
    useForm<ProfileFormData>({ resolver: zodResolver(ProfileSchema) });

  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.get("/api/me/");
        reset({
          username: data.username ?? "",
          first_name: data.first_name ?? "",
          last_name: data.last_name ?? "",
          email: data.email ?? "",
          profile: {
            phone: data.profile?.phone ?? "",
            bio: data.profile?.bio ?? "",
          },
        });
      } catch (err: unknown) {
        setErrorMsg(extractErrorMessage(err));
      } finally {
        setLoading(false);
      }
    })();
  }, [reset]);

  async function onSubmit(values: ProfileFormData) {
    setSaveMsg(null);
    setErrorMsg(null);
    try {
      const { data } = await api.patch("/api/me/", values);
      reset({
        username: data.username ?? "",
        first_name: data.first_name ?? "",
        last_name: data.last_name ?? "",
        email: data.email ?? "",
        profile: { phone: data.profile?.phone ?? "", bio: data.profile?.bio ?? "" },
      });
      setSaveMsg("Perfil actualizado ✅");
    } catch (err: unknown) {
      setErrorMsg(extractErrorMessage(err));
    }
  }

  if (loading) return <div style={{ padding: 16 }}>Cargando perfil…</div>;

  return (
  <div className="container">
    <h1>Mi perfil</h1>
    <div className="card">
      {saveMsg && <div className="alert ok">{saveMsg}</div>}
      {errorMsg && <div className="alert err">{errorMsg}</div>}

      {loading ? (
        <div>Cargando perfil…</div>
      ) : (
        <form onSubmit={handleSubmit(onSubmit)} className="grid" style={{gap:16}}>
          <div>
            <label className="label">Usuario</label>
            <input className="input" {...register("username")} disabled />
          </div>

          <div className="grid cols">
            <div>
              <label className="label">Nombre</label>
              <input className="input" {...register("first_name")} />
              {errors.first_name && <span className="small-err">{errors.first_name.message}</span>}
            </div>
            <div>
              <label className="label">Apellido</label>
              <input className="input" {...register("last_name")} />
              {errors.last_name && <span className="small-err">{errors.last_name.message}</span>}
            </div>
          </div>

          <div>
            <label className="label">Email</label>
            <input className="input" type="email" {...register("email")} />
            {errors.email && <span className="small-err">{errors.email.message}</span>}
          </div>

          <div className="grid cols">
            <div>
              <label className="label">Teléfono</label>
              <input className="input" placeholder="+591..." {...register("profile.phone")} />
            </div>
            <div>
              <label className="label">Bio</label>
              <textarea className="textarea" rows={4} placeholder="Tu especialidad…" {...register("profile.bio")} />
              {errors.profile?.bio && <span className="small-err">{errors.profile.bio.message}</span>}
            </div>
          </div>

          <div className="row">
            <button className="btn primary" disabled={isSubmitting} type="submit">
              {isSubmitting ? "Guardando…" : "Guardar cambios"}
            </button>
            <button className="btn" type="button" onClick={() => window.location.reload()}>
              Deshacer
            </button>
          </div>
        </form>
      )}
    </div>
  </div>
);
}