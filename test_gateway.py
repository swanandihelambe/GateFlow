from app.gateway import resolve_route


print(resolve_route("/api/users"))
print(resolve_route("/api/orders"))
print(resolve_route("/api/unknown"))