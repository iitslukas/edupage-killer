import MockAdapter from "axios-mock-adapter";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import apiClient from "../client";

describe("apiClient request interceptor", () => {
  let mock: MockAdapter;

  beforeEach(() => {
    mock = new MockAdapter(apiClient);
    localStorage.clear();
  });

  afterEach(() => {
    mock.restore();
  });

  it("attaches Bearer token when access_token is in localStorage", async () => {
    localStorage.setItem("access_token", "test-access-token");
    let capturedAuth: string | undefined;
    mock.onGet("/probe").reply((config) => {
      capturedAuth = config.headers?.["Authorization"] as string | undefined;
      return [200, {}];
    });
    await apiClient.get("/probe");
    expect(capturedAuth).toBe("Bearer test-access-token");
  });

  it("omits Authorization header when no token in localStorage", async () => {
    let capturedAuth: string | undefined;
    mock.onGet("/probe").reply((config) => {
      capturedAuth = config.headers?.["Authorization"] as string | undefined;
      return [200, {}];
    });
    await apiClient.get("/probe");
    expect(capturedAuth).toBeUndefined();
  });
});
