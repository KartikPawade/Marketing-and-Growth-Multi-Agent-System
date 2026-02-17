const API_BASE = '/api';

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const url = path.startsWith('http') ? path : `${API_BASE}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  if (res.status === 204) return undefined as T;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || res.statusText || 'Request failed');
  return data as T;
}

export const api = {
  health: () => request<{ status: string }>('/health'),

  brands: {
    list: () => request<BrandSummary[]>('/brands'),
    create: (body: Record<string, unknown>) =>
      request<BrandResponse>('/brands', { method: 'POST', body: JSON.stringify(body) }),
    get: (id: string) => request<BrandResponse>(`/brands/${id}`),
    update: (id: string, body: Record<string, unknown>) =>
      request<BrandResponse>(`/brands/${id}`, { method: 'PUT', body: JSON.stringify(body) }),
    delete: (id: string) =>
      request<void>(`/brands/${id}`, { method: 'DELETE' }),
  },

  campaigns: {
    create: (body: { brand_id: string; goal: string; target_audience: string; budget: number }) =>
      request<CampaignResponse>('/campaigns', { method: 'POST', body: JSON.stringify(body) }),
  },
};

export interface BrandSummary {
  id: string;
  name: string;
}

export interface BrandResponse {
  id: string;
  name: string;
  description: string;
  industry: string;
  tone: string;
  usp: string;
  target_audience: string;
  memory?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface CampaignResponse {
  id: string;
  status: string;
  research?: unknown;
}
