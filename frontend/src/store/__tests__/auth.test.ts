import { beforeEach, describe, expect, it } from "vitest";
import { useAuthStore } from "../auth";
import type { User } from "@/types";

const mockUser: User = {
  id: 1,
  email: "test@example.com",
  full_name: "Test User",
  role: "student",
  avatar: null,
};

describe("useAuthStore", () => {
  beforeEach(() => {
    useAuthStore.setState({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
    });
    localStorage.clear();
  });

  describe("setAuth", () => {
    it("sets user, tokens, and isAuthenticated to true", () => {
      useAuthStore.getState().setAuth(mockUser, "access123", "refresh456");
      const state = useAuthStore.getState();
      expect(state.user).toEqual(mockUser);
      expect(state.accessToken).toBe("access123");
      expect(state.refreshToken).toBe("refresh456");
      expect(state.isAuthenticated).toBe(true);
    });

    it("writes tokens to localStorage", () => {
      useAuthStore.getState().setAuth(mockUser, "access123", "refresh456");
      expect(localStorage.getItem("access_token")).toBe("access123");
      expect(localStorage.getItem("refresh_token")).toBe("refresh456");
    });
  });

  describe("setUser", () => {
    it("updates user without changing isAuthenticated", () => {
      useAuthStore.setState({ isAuthenticated: true, user: mockUser });
      useAuthStore.getState().setUser({ ...mockUser, full_name: "Updated Name" });
      const state = useAuthStore.getState();
      expect(state.user?.full_name).toBe("Updated Name");
      expect(state.isAuthenticated).toBe(true);
    });
  });

  describe("logout", () => {
    it("clears all auth state", () => {
      useAuthStore.getState().setAuth(mockUser, "access123", "refresh456");
      useAuthStore.getState().logout();
      const state = useAuthStore.getState();
      expect(state.user).toBeNull();
      expect(state.accessToken).toBeNull();
      expect(state.refreshToken).toBeNull();
      expect(state.isAuthenticated).toBe(false);
    });

    it("removes tokens from localStorage", () => {
      localStorage.setItem("access_token", "access123");
      localStorage.setItem("refresh_token", "refresh456");
      useAuthStore.getState().logout();
      expect(localStorage.getItem("access_token")).toBeNull();
      expect(localStorage.getItem("refresh_token")).toBeNull();
    });
  });
});
