1. Q: The application is a MFA application. I need to be able to plot a diagram that illustrates the flow of the multi-factor authentication process. I need to know how to plot in mermaid first.

-> Quick task: Learn to plot in mermaid (tutorial) (estimate 20mins)

**First idea on authentication flow (system)**
```mermaid
graph LR
    A[User] --->|u,p,pin| B[Login Page]
    B --->|u,p,pin| C[Authentication Server]
    C --->|token| A
```

**Full login flow with MFA (backend)**

*System flow:*
```mermaid
graph LR
    A(FE) -->|1: u,p,pin| B[Authentication Service] 
    B -->|2: fetch data| C[Database]
    C -->|3: validate| B
    B -->|4: generate token| D[Token Service]
    D -->|5: return token| A
```

*Authentication Service flow:*
```mermaid
graph LR
    A(FE) -->|1: u,p,pin| B[main]
    B -.->|2: query user| C[Database]
    C -.->|3: return user data| B
    B --> D{ifUserExists}
    D -->|yes| E[validate password]
    E -->|6: validate| B
    D -->|no| F[return error]
    E --> G{ifPasswordValid}
    G -->|yes| H[Second Factor Service]
    G -->|no| F[return error]
    H -->I{ifSecondFactorValid}
    I -->|yes| J[generate token]
    I -->|no| F[return error]
    J -->|7: return token| A
```

This is the initial idea of the backend flow for the multi-factor authentication process. I will focus on the first factor authentication at the beginning stage which is to handle username, password, and pin validation. The second factor will be handled after the first factor is validated successfully.

2. Q: I will briefly think about the backend with design and code logic. 

**Idea:** The backend should have an object to store current user's session information, including user's authentication status and any relevant timestamps for session management. As authenticating, that object will be updated to reflect the current state of the user's authentication process. and to have a clean program, those statuses should be handled modularly, with separate functions for each step of the authentication process. At the end of the program, one function would check if the object has all the necessary information to determine if the user is authenticated or not. A logging pipeline should also be implemented to track the flow of the authentication process.

**Object idea**
```mermaid
classDiagram
    class AuthenticationSession {
        - userId: String
        - isPasswordValid: Boolean
        - isPinValid: Boolean
        - lastLoginAttempt: DateTime
        - secondFactorValidated: Boolean
        + validatePassword(password: String)
        + validatePin(pin: String)
        + updateLastLoginAttempt()
        + setSecondFactorValidated()
    }
```

-> The last checkout function will validate all conditions and if all are met, it will return a successful authentication status. 

3. Let me think about the techs and stacks that can be implemented. 

A: Front end: I need 4 screens (login, register, second factor, and session status). I can use HTML, CSS, and JavaScript for the front end as they are simple and easy to implement.

B: Backend: I will use Flask for the backend framework. Flask is a good choice for simplicity and flexibility. I will add more techs that support the application.

C: Database: I will use SQLite for the database as it is lightweight and easy to set up. 

**Table of techs/stacks**

| Problem | Technology/Stack |
|---------|------------------|
| Frontend | HTML, CSS, JavaScript |
| Styling (optional) | Bootstrap |
| Craft request and receive response (frontend) | Axios or Fetch API |
| Backend | Flask |
| Query database | SQLAlchemy |
| Hashing | bcrypt |
| Token generation (optional) | PyJWT |
| Client-side token storage | HttpOnly cookies or localStorage (with caution) |
| Database | SQLite |
| Containerization | Docker |
| Database management | SQLite Studio |
| Testing | pytest | 
| Environment variables | python-dotenv |
---


# CODING SESSION TO TEST THE INITIAL IDEA


