import axios from 'axios'
import type { AxiosResponse } from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response: AxiosResponse) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ---------- 财务加班 ----------
export interface OvertimeRecord {
  id: number
  employee_name: string
  job_title: string
  job_level: string
  overtime_hours: number
  overtime_minutes: number
  overtime_days: number
  overtime_rate: number
  overtime_amount: number
  overtime_detail: string
  attendance_month: string
  created_at: string
  updated_at: string
}

export interface OvertimeStats {
  total_employees: number
  overtime_employees: number
  total_hours: number
  total_days: number
  total_amount: number
  avg_hours: number
}

export interface LevelStats {
  job_level: string
  count: number
  total_hours: number
  total_amount: number
}

export interface TopEmployee {
  employee_name: string
  job_title: string
  job_level: string
  overtime_hours: number
  overtime_amount: number
}

export const uploadAttendance = (file: File, month?: string) => {
  const formData = new FormData()
  formData.append('file', file)
  if (month) formData.append('month', month)
  return api.post('/financial/upload-attendance', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const getOvertimeRecords = (params: {
  page?: number
  page_size?: number
  month?: string
  keyword?: string
  sort_field?: string
  sort_order?: string
}) => {
  return api.get('/financial/overtime-records', { params })
}

export const getOvertimeStats = (month?: string) => {
  return api.get('/financial/overtime-stats', { params: { month } })
}

export const deleteOvertimeRecords = (params: { ids?: number[]; month?: string }) => {
  return api.delete('/financial/overtime-records', { params })
}

// ---------- 考勤扣款 ----------
export interface DeductionRecord {
  id: number
  employee_name: string
  job_title: string
  job_level: string
  level_type: string
  total_late_count: number
  late_within_10_count: number
  late_over_10_count: number
  late_over_60_count: number
  morning_missing_count: number
  evening_missing_count: number
  early_leave_count: number
  total_deduction: number
  attendance_month: string
  created_at: string
  updated_at: string
}

export interface DeductionStats {
  total_employees: number
  deduction_employees: number
  total_late_count: number
  late_within_10_count: number
  late_over_10_count: number
  late_over_60_count: number
  morning_missing_count: number
  evening_missing_count: number
  early_leave_count: number
  total_deduction: number
}

export interface LevelDeductionStats {
  level_type: string
  count: number
  total_late: number
  total_deduction: number
}

export interface TopDeductionEmployee {
  employee_name: string
  job_title: string
  level_type: string
  total_late_count: number
  total_deduction: number
}

export const uploadAttendanceDeduction = (file: File, month?: string) => {
  const formData = new FormData()
  formData.append('file', file)
  if (month) formData.append('month', month)
  return api.post('/financial/attendance/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const getDeductionRecords = (params: {
  page?: number
  page_size?: number
  month?: string
  keyword?: string
}) => {
  return api.get('/financial/attendance/records', { params })
}

export const getDeductionStats = (month?: string) => {
  return api.get('/financial/attendance/stats', { params: { month } })
}

export const deleteDeductionRecords = (params: { ids?: number[]; month?: string }) => {
  return api.delete('/financial/attendance/records', { params })
}

export const exportDeductionRecords = async (month?: string, keyword?: string) => {
  const params = new URLSearchParams()
  if (month) params.append('month', month)
  if (keyword) params.append('keyword', keyword)

  const response = await fetch(`/api/financial/attendance/export?${params.toString()}`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token') || ''}`
    }
  })

  if (!response.ok) throw new Error('导出失败')

  const blob = await response.blob()
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `attendance_deduction_${month || 'all'}_${Date.now()}.xlsx`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  window.URL.revokeObjectURL(url)
}

export default api
