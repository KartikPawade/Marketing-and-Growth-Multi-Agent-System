import { useState, useEffect } from 'react'
import { api, BrandResponse, BrandSummary } from '../api'

function fetchAllBrands(
  setList: (b: BrandSummary[]) => void,
  setLoading: (v: boolean) => void,
  setError: (e: string | null) => void
) {
  setLoading(true)
  setError(null)
  api.brands
    .list()
    .then(setList)
    .catch((err) => setError(err instanceof Error ? err.message : 'Failed to load brands'))
    .finally(() => setLoading(false))
}

export default function BrandsTab() {
  const [allBrands, setAllBrands] = useState<BrandSummary[]>([])
  const [listLoading, setListLoading] = useState(false)
  const [listError, setListError] = useState<string | null>(null)
  const [brandId, setBrandId] = useState('')
  const [brand, setBrand] = useState<BrandResponse | null>(null)
  const [createForm, setCreateForm] = useState({
    name: '',
    description: '',
    industry: '',
    tone: '',
    usp: '',
    target_audience: '',
  })
  const [updateForm, setUpdateForm] = useState({
    name: '',
    description: '',
    industry: '',
    tone: '',
    usp: '',
    target_audience: '',
  })
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)
  const [loading, setLoading] = useState<string | null>(null)

  useEffect(() => {
    fetchAllBrands(setAllBrands, setListLoading, setListError)
  }, [])

  const refreshAllBrands = () => {
    fetchAllBrands(setAllBrands, setListLoading, setListError)
  }

  const loadBrandById = async (id: string) => {
    setBrandId(id)
    setLoading('get')
    setMessage(null)
    setBrand(null)
    try {
      const res = await api.brands.get(id)
      setBrand(res)
      setUpdateForm({
        name: res.name,
        description: res.description,
        industry: res.industry,
        tone: res.tone,
        usp: res.usp,
        target_audience: res.target_audience,
      })
      showMsg('success', 'Brand loaded')
    } catch (err) {
      showMsg('error', err instanceof Error ? err.message : 'Get failed')
    } finally {
      setLoading(null)
    }
  }

  const showMsg = (type: 'success' | 'error', text: string) => {
    setMessage({ type, text })
    setTimeout(() => setMessage(null), 5000)
  }

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading('create')
    setMessage(null)
    try {
      const res = await api.brands.create(createForm)
      showMsg('success', `Brand created: ${res.id}`)
      setBrand(res)
      setBrandId(res.id)
      setUpdateForm({
        name: res.name,
        description: res.description,
        industry: res.industry,
        tone: res.tone,
        usp: res.usp,
        target_audience: res.target_audience,
      })
      refreshAllBrands()
    } catch (err) {
      showMsg('error', err instanceof Error ? err.message : 'Create failed')
    } finally {
      setLoading(null)
    }
  }

  const handleGet = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!brandId.trim()) return
    setLoading('get')
    setMessage(null)
    setBrand(null)
    try {
      const res = await api.brands.get(brandId.trim())
      setBrand(res)
      setUpdateForm({
        name: res.name,
        description: res.description,
        industry: res.industry,
        tone: res.tone,
        usp: res.usp,
        target_audience: res.target_audience,
      })
      showMsg('success', 'Brand loaded')
    } catch (err) {
      showMsg('error', err instanceof Error ? err.message : 'Get failed')
    } finally {
      setLoading(null)
    }
  }

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!brandId.trim()) return
    setLoading('update')
    setMessage(null)
    try {
      const res = await api.brands.update(brandId.trim(), updateForm)
      setBrand(res)
      showMsg('success', 'Brand updated')
    } catch (err) {
      showMsg('error', err instanceof Error ? err.message : 'Update failed')
    } finally {
      setLoading(null)
    }
  }

  const handleDelete = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!brandId.trim()) return
    if (!confirm('Delete this brand?')) return
    setLoading('delete')
    setMessage(null)
    try {
      await api.brands.delete(brandId.trim())
      setBrand(null)
      setBrandId('')
      showMsg('success', 'Brand deleted')
      refreshAllBrands()
    } catch (err) {
      showMsg('error', err instanceof Error ? err.message : 'Delete failed')
    } finally {
      setLoading(null)
    }
  }

  return (
    <>
      <h1 className="tab-title">Brands</h1>
      {message && (
        <div className={`message ${message.type}`} style={{ marginBottom: '1rem' }}>
          {message.text}
        </div>
      )}

      <div className="card tab-section">
        <div className="tab-section-title">All brands (GET /brands)</div>
        <div className="form-actions" style={{ marginBottom: '0.75rem' }}>
          <button
            type="button"
            className="btn btn-ghost"
            onClick={refreshAllBrands}
            disabled={listLoading}
          >
            {listLoading ? 'Loading…' : 'Refresh list'}
          </button>
        </div>
        {listError && (
          <div className="message error" style={{ marginBottom: '0.75rem' }}>
            {listError}
          </div>
        )}
        {allBrands.length === 0 && !listLoading && !listError && (
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>No brands yet. Create one below.</p>
        )}
        {allBrands.length > 0 && (
          <ul className="brands-list">
            {allBrands.map((b) => (
              <li key={b.id} className="brands-list-item">
                <button
                  type="button"
                  className={`brands-list-btn ${brandId === b.id ? 'active' : ''}`}
                  onClick={() => loadBrandById(b.id)}
                >
                  <span className="brands-list-name">{b.name || '(Unnamed)'}</span>
                  <span className="brands-list-id">{b.id}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="card tab-section">
        <div className="tab-section-title">Create brand (POST /brands)</div>
        <form onSubmit={handleCreate}>
          <div className="form-grid">
            <div className="form-group full">
              <label className="label">Name</label>
              <input
                value={createForm.name}
                onChange={(e) => setCreateForm((f) => ({ ...f, name: e.target.value }))}
                placeholder="Brand name"
              />
            </div>
            <div className="form-group full">
              <label className="label">Description</label>
              <textarea
                value={createForm.description}
                onChange={(e) => setCreateForm((f) => ({ ...f, description: e.target.value }))}
                placeholder="Short description"
                rows={2}
              />
            </div>
            <div className="form-group">
              <label className="label">Industry</label>
              <input
                value={createForm.industry}
                onChange={(e) => setCreateForm((f) => ({ ...f, industry: e.target.value }))}
                placeholder="e.g. Tech"
              />
            </div>
            <div className="form-group">
              <label className="label">Tone</label>
              <input
                value={createForm.tone}
                onChange={(e) => setCreateForm((f) => ({ ...f, tone: e.target.value }))}
                placeholder="e.g. Professional"
              />
            </div>
            <div className="form-group">
              <label className="label">USP</label>
              <input
                value={createForm.usp}
                onChange={(e) => setCreateForm((f) => ({ ...f, usp: e.target.value }))}
                placeholder="Unique selling point"
              />
            </div>
            <div className="form-group">
              <label className="label">Target audience</label>
              <input
                value={createForm.target_audience}
                onChange={(e) => setCreateForm((f) => ({ ...f, target_audience: e.target.value }))}
                placeholder="e.g. B2B"
              />
            </div>
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={!!loading}>
              {loading === 'create' ? 'Creating…' : 'Create brand'}
            </button>
          </div>
        </form>
      </div>

      <div className="card tab-section">
        <div className="tab-section-title">Get brand (GET /brands/:id)</div>
        <form onSubmit={handleGet} style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div className="form-group">
            <label className="label">Brand ID</label>
            <input
              className="input-id"
              value={brandId}
              onChange={(e) => setBrandId(e.target.value)}
              placeholder="e.g. brand_abc123"
            />
          </div>
          <button type="submit" className="btn btn-primary" disabled={!!loading}>
            {loading === 'get' ? 'Loading…' : 'Get brand'}
          </button>
        </form>
      </div>

      {brand && (
        <>
          <div className="card tab-section">
            <div className="tab-section-title">Update brand (PUT /brands/:id)</div>
            <form onSubmit={handleUpdate}>
              <div className="form-grid">
                <div className="form-group full">
                  <label className="label">Name</label>
                  <input
                    value={updateForm.name}
                    onChange={(e) => setUpdateForm((f) => ({ ...f, name: e.target.value }))}
                  />
                </div>
                <div className="form-group full">
                  <label className="label">Description</label>
                  <textarea
                    value={updateForm.description}
                    onChange={(e) => setUpdateForm((f) => ({ ...f, description: e.target.value }))}
                    rows={2}
                  />
                </div>
                <div className="form-group">
                  <label className="label">Industry</label>
                  <input
                    value={updateForm.industry}
                    onChange={(e) => setUpdateForm((f) => ({ ...f, industry: e.target.value }))}
                  />
                </div>
                <div className="form-group">
                  <label className="label">Tone</label>
                  <input
                    value={updateForm.tone}
                    onChange={(e) => setUpdateForm((f) => ({ ...f, tone: e.target.value }))}
                  />
                </div>
                <div className="form-group">
                  <label className="label">USP</label>
                  <input
                    value={updateForm.usp}
                    onChange={(e) => setUpdateForm((f) => ({ ...f, usp: e.target.value }))}
                  />
                </div>
                <div className="form-group">
                  <label className="label">Target audience</label>
                  <input
                    value={updateForm.target_audience}
                    onChange={(e) => setUpdateForm((f) => ({ ...f, target_audience: e.target.value }))}
                  />
                </div>
              </div>
              <div className="form-actions">
                <button type="submit" className="btn btn-primary" disabled={!!loading}>
                  {loading === 'update' ? 'Updating…' : 'Update brand'}
                </button>
              </div>
            </form>
          </div>
          <div className="card tab-section">
            <div className="tab-section-title">Delete brand (DELETE /brands/:id)</div>
            <form onSubmit={handleDelete}>
              <button type="submit" className="btn btn-danger" disabled={!!loading}>
                {loading === 'delete' ? 'Deleting…' : 'Delete brand'}
              </button>
            </form>
          </div>
          <div className="card tab-section">
            <div className="tab-section-title">Current brand</div>
            <pre style={{ fontSize: '0.8rem', overflow: 'auto', color: 'var(--text-secondary)' }}>
              {JSON.stringify(brand, null, 2)}
            </pre>
          </div>
        </>
      )}
    </>
  )
}
