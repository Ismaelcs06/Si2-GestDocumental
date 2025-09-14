// src/pages/ChangePasswordPage.tsx
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { api } from "../lib/api";
import { useState } from "react";
import type { AxiosError } from "axios";

const Schema = z.object({
  current_password: z.string().min(1, "Requerida"),
  new_password: z
    .string()
    .min(8, "Mínimo 8 caracteres")
    .regex(/[A-Z]/, "Al menos 1 mayúscula")
    .regex(/[a-z]/, "Al menos 1 minúscula")
    .regex(/\d/, "Al menos 1 número")
    .regex(/[^A-Za-z0-9]/, "Al menos 1 símbolo"),
  confirm_password: z.string().min(8),
}).refine((d) => d.new_password === d.confirm_password, {
  path: ["confirm_password"],
  message: "No coincide con la nueva contraseña",
});

type Form = z.infer<typeof Schema>;

function extractErrorMessage(err: unknown): string {
  const DEFAULT = "No se pudo cambiar la contraseña";
  const ax = err as AxiosError<
    | { detail?: string; current_password?: string[]; new_password?: string[] }
    | undefined
  >;
  // priorizamos mensajes de campos si DRF los envía
  const data = ax?.response?.data;
  if (data?.current_password?.[0]) return data.current_password[0];
  if (data?.new_password?.[0]) return data.new_password[0];
  if (typeof data?.detail === "string") return data.detail;
  return DEFAULT;
}

export default function ChangePasswordPage() {
  const [ok, setOk] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<Form>({ resolver: zodResolver(Schema) });

  async function onSubmit(v: Form) {
    setOk(null);
    setErr(null);
    try {
      await api.post("/api/auth/change-password/", v);
      setOk("Contraseña actualizada ✅");
      reset({ current_password: "", new_password: "", confirm_password: "" });
    } catch (e: unknown) {
      setErr(extractErrorMessage(e));
    }
  }

  return (
    <div className="container">
      <h1>Cambiar contraseña</h1>
      <div className="card">
        {ok && <div className="alert ok">{ok}</div>}
        {err && <div className="alert err">{err}</div>}

        <form onSubmit={handleSubmit(onSubmit)} className="grid" style={{ gap: 16 }}>
          <div>
            <label className="label">Actual</label>
            <input className="input" type="password" {...register("current_password")} />
            {errors.current_password && (
              <span className="small-err">{errors.current_password.message}</span>
            )}
          </div>

          <div>
            <label className="label">Nueva</label>
            <input className="input" type="password" {...register("new_password")} />
            {errors.new_password && (
              <span className="small-err">{errors.new_password.message}</span>
            )}
          </div>

          <div>
            <label className="label">Confirmar</label>
            <input className="input" type="password" {...register("confirm_password")} />
            {errors.confirm_password && (
              <span className="small-err">{errors.confirm_password.message}</span>
            )}
          </div>

          <div className="row">
            <button className="btn primary" disabled={isSubmitting}>
              {isSubmitting ? "Guardando…" : "Cambiar contraseña"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
