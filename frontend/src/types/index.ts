export type UserRole = "student" | "parent" | "teacher" | "admin";

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  avatar: string | null;
}

export interface SchoolClass {
  id: number;
  name: string;
  grade: number;
  section: string;
  year: number;
  student_count: number;
}

export interface Subject {
  id: number;
  name: string;
  short_name: string;
  color: string;
}

export interface Period {
  id: number;
  number: number;
  start_time: string;
  end_time: string;
  name: string;
}

export interface TimetableEntry {
  id: number;
  subject: Subject;
  teacher: number | null;
  teacher_name: string;
  school_class: number;
  room: number | null;
  room_name: string;
  period: number;
  period_info: Period;
  day: number;
  week_type: string;
}

export interface AttendanceRecord {
  id: number;
  student: number;
  student_name: string;
  date: string;
  period: number;
  subject: number | null;
  subject_name: string;
  status: "present" | "absent" | "late" | "excused";
  note: string;
}

export type MaterialType = "handout" | "presentation" | "exercise" | "video" | "link" | "other";

export interface Material {
  id: number;
  title: string;
  description: string;
  material_type: MaterialType;
  file: string | null;
  url: string;
  subject: number | null;
  uploaded_by: number;
  uploaded_by_name: string;
  visibility: string;
  created_at: string;
  lesson_date: string | null;
  comment_count: number;
}

export interface Channel {
  id: number;
  name: string;
  channel_type: "class" | "subject" | "direct" | "group";
  description: string;
  school_class: number | null;
  member_count: number;
  last_message: { content: string; author: string; at: string } | null;
}

export interface Message {
  id: number;
  channel: number;
  author: number;
  author_name: string;
  content: string;
  attachment: string | null;
  reply_to: number | null;
  created_at: string;
  is_deleted: boolean;
  reaction_count: number;
}

export type AssignmentType = "homework" | "exam" | "quiz" | "project" | "lab";

export interface Assignment {
  id: number;
  title: string;
  description: string;
  assignment_type: AssignmentType;
  subject: number;
  subject_name: string;
  school_class: number;
  assigned_by: number;
  assigned_by_name: string;
  due_date: string;
  max_score: number | null;
  is_graded: boolean;
  is_overdue: boolean;
}

export interface Submission {
  id: number;
  assignment: number;
  student: number;
  student_name: string;
  submitted_at: string;
  status: "pending" | "submitted" | "late" | "graded";
  score: number | null;
  feedback: string;
}

export interface Grade {
  id: number;
  student: number;
  student_name: string;
  subject: number;
  subject_name: string;
  value: number;
  max_value: number;
  label: string;
  date: string;
  is_final: boolean;
}

export interface Note {
  id: number;
  title: string;
  content: string;
  author: number;
  author_name: string;
  subject: number | null;
  subject_name: string;
  visibility: "private" | "class" | "school";
  lesson_date: string | null;
  created_at: string;
  updated_at: string;
  tags: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface AuthTokens {
  access: string;
  refresh: string;
}
