// types/index.ts
export interface User {
  id: number;
  name: string;
  email: string;
}

export interface ApiResponse<T = any> {
  data: T;
  success: boolean;
  message?: string;
}
