# JARVIS — Test Credentials

## Pre-seeded test user (for backend Bearer-token / cookie-based testing)

| Field           | Value                                                   |
|-----------------|---------------------------------------------------------|
| `user_id`       | `user_cb59d95cccf9`                                     |
| `email`         | `jarvis.tester@example.com`                             |
| `name`          | Tony Stark                                              |
| `picture`       | https://i.pravatar.cc/64?u=jarvis                       |
| `session_token` | `test_jarvis_1777130060331`                             |
| Expires         | ~2026-05-02 (7 days from creation 2026-04-25)           |

## How to use

### As Authorization header
```bash
curl -H "Authorization: Bearer test_jarvis_1777130060331" \
     "$URL/api/auth/me"
```

### As cookie (browser/Playwright)
```python
await page.context.add_cookies([{
    "name": "session_token",
    "value": "test_jarvis_1777130060331",
    "domain": "<your-preview-domain>",
    "path": "/",
    "httpOnly": True,
    "secure": True,
    "sameSite": "None",
}])
```

## Re-seed if expired
```bash
mongosh --quiet --eval '
use("jarvis_db");
db.users.deleteMany({email: /jarvis\.tester/});
db.user_sessions.deleteMany({session_token: /test_jarvis_/});
var userId = "user_" + Math.random().toString(16).slice(2, 14);
var token   = "test_jarvis_" + Date.now();
db.users.insertOne({
  user_id: userId, email: "jarvis.tester@example.com",
  name: "Tony Stark", picture: "https://i.pravatar.cc/64?u=jarvis",
  created_at: new Date()
});
db.user_sessions.insertOne({
  user_id: userId, session_token: token,
  expires_at: new Date(Date.now() + 7*24*60*60*1000),
  created_at: new Date()
});
print("USER_ID=" + userId);
print("TOKEN="   + token);
'
```

## Cleanup
```bash
mongosh --quiet --eval '
use("jarvis_db");
db.users.deleteMany({email: /jarvis\.tester|test\.user\./});
db.user_sessions.deleteMany({session_token: /test_jarvis_|test_session/});
'
```

## Notes
- Auth uses Emergent-managed Google OAuth in production (no app-managed passwords).
- The full OAuth round-trip cannot be exercised in CI — tests bypass by directly inserting `users` + `user_sessions` documents via mongosh/pymongo.
- Anonymous users (no token) share a single `"anonymous"` session bucket — that's by design for unauthenticated experimentation but is documented as a soft caveat.
