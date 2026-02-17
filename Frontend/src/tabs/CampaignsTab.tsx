import { useState } from 'react'
import { api, CampaignResponse } from '../api'

export default function CampaignsTab() {
  const [form, setForm] = useState({
    brand_id: '',
    goal: '',
    target_audience: '',
    budget: '',
  })
  const [result, setResult] = useState<CampaignResponse | null>(null)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const budget = parseFloat(form.budget)
    if (isNaN(budget) || budget < 0) {
      setMessage({ type: 'error', text: 'Budget must be a positive number' })
      return
    }
    setLoading(true)
    setMessage(null)
    setResult(null)
    try {
      const res = await api.campaigns.create({
        brand_id: form.brand_id,
        goal: form.goal,
        target_audience: form.target_audience,
        budget,
      })
      setResult(res)
      setMessage({ type: 'success', text: `Campaign created: ${res.id} (${res.status})` })
    } catch (err) {
      setMessage({
        type: 'error',
        text: err instanceof Error ? err.message : 'Create campaign failed',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <h1 className="tab-title">Campaigns</h1>
      {message && (
        <div className={`message ${message.type}`} style={{ marginBottom: '1rem' }}>
          {message.text}
        </div>
      )}

      <div className="card tab-section">
        <div className="tab-section-title">Create campaign (POST /campaigns)</div>
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group full">
              <label className="label">Brand ID</label>
              <input
                value={form.brand_id}
                onChange={(e) => setForm((f) => ({ ...f, brand_id: e.target.value }))}
                placeholder="e.g. brand_abc123"
                required
              />
            </div>
            <div className="form-group full">
              <label className="label">Goal</label>
              <input
                value={form.goal}
                onChange={(e) => setForm((f) => ({ ...f, goal: e.target.value }))}
                placeholder="Campaign goal"
                required
              />
            </div>
            <div className="form-group">
              <label className="label">Target audience</label>
              <input
                value={form.target_audience}
                onChange={(e) => setForm((f) => ({ ...f, target_audience: e.target.value }))}
                placeholder="e.g. B2B decision makers"
                required
              />
            </div>
            <div className="form-group">
              <label className="label">Budget</label>
              <input
                type="number"
                min="0"
                step="0.01"
                value={form.budget}
                onChange={(e) => setForm((f) => ({ ...f, budget: e.target.value }))}
                placeholder="0.00"
                required
              />
            </div>
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Creating…' : 'Create campaign'}
            </button>
          </div>
        </form>
      </div>

      {result && (
        <div className="card tab-section">
          <div className="tab-section-title">Response</div>
          <pre style={{ fontSize: '0.85rem', overflow: 'auto', color: 'var(--text-secondary)' }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </>
  )
}
