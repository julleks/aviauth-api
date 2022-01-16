from uuid import UUID, uuid4

from jose import jwt
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from app.core.config import settings
from app.core.datetime import datetime

__all__ = ["IDToken"]


class IDToken(SQLModel, table=True):
    """
    The ID Token is a security token that contains Claims about the Authentication of an
    End-User by an Authorization Server when using a Client, and potentially other
    requested Claims. The ID Token is represented as a JSON Web Token (JWT).

    See OpenID Connect specification:
        https://openid.net/specs/openid-connect-core-1_0.html#IDToken
    """

    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
        nullable=False,
        sa_column_kwargs=dict(unique=True),
    )
    user_id: UUID = Field(foreign_key="user.id")
    client_id: str = Field(foreign_key="application.client_id", nullable=True)
    application: "Application" = Relationship(back_populates="id_tokens")
    token: str = Field(primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)), default_factory=datetime.now
    )
    revoked_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)), nullable=True
    )
    expires_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    scope: str = Field(index=False)

    @property
    def is_active(self) -> bool:
        return bool((not self.revoked_at) and (self.expires_at > datetime.now()))

    def get_token_jwt(self):
        """The following Claims are used within the ID Token for all OAuth 2.0 flows used
        by OpenID Connect:

        iss
            REQUIRED. Issuer Identifier for the Issuer of the response.
            The iss value is a case-sensitive URL using the https scheme
            that contains scheme, host, and optionally, port number and
            path components and no query or fragment components.

        sub
            REQUIRED. Subject Identifier. A locally unique and never
            reassigned identifier within the Issuer for the End-User,
            which is intended to be consumed by the Client, e.g., 24400320
            or AItOawmwtWwcT0k51BayewNvutrJUqsvl6qs7A4. It MUST NOT exceed
            255 ASCII characters in length. The sub value is a case-sensitive
            string.

        aud
            REQUIRED. Audience(s) that this ID Token is intended for.
            It MUST contain the OAuth 2.0 client_id of the Relying Party
            as an audience value. It MAY also contain identifiers for
            other audiences. In the general case, the aud value is
            an array of case-sensitive strings. In the common special
            case when there is one audience, the aud value MAY be a single
            case-sensitive string.

        exp
            REQUIRED. Expiration time on or after which the ID Token
            MUST NOT be accepted for processing. The processing of
            this parameter requires that the current date/time MUST
            be before the expiration date/time listed in the value.
            Implementers MAY provide for some small leeway, usually
            no more than a few minutes, to account for clock skew.
            Its value is a JSON number representing the number of
            seconds from 1970-01-01T0:0:0Z as measured in UTC until
            the date/time. See [RFC3339] for details regarding
            date/times in general and UTC in particular.

        iat
            REQUIRED. Time at which the JWT was issued. Its value is
            a JSON number representing the number of seconds from
            1970-01-01T0:0:0Z as measured in UTC until the date/time.

        auth_time
            Time when the End-User authentication occurred. Its value
            is a JSON number representing the number of seconds from
            1970-01-01T0:0:0Z as measured in UTC until the date/time.
            When a max_age request is made or when auth_time is requested
            as an Essential Claim, then this Claim is REQUIRED; otherwise,
            its inclusion is OPTIONAL. (The auth_time Claim semantically
            corresponds to the OpenID 2.0 PAPE [OpenID.PAPE] auth_time
            response parameter.)

        nonce
            String value used to associate a Client session with
            an ID Token, and to mitigate replay attacks. The value
            is passed through unmodified from the Authentication
            Request to the ID Token. If present in the ID Token,
            Clients MUST verify that the nonce Claim Value is
            equal to the value of the nonce parameter sent in the
            Authentication Request. If present in the Authentication
            Request, Authorization Servers MUST include a nonce Claim
            in the ID Token with the Claim Value being the nonce value
            sent in the Authentication Request. Authorization Servers
            SHOULD perform no other processing on nonce values used.
            The nonce value is a case-sensitive string.

        acr
            OPTIONAL. Authentication Context Class Reference.
            String specifying an Authentication Context Class
            Reference value that identifies the Authentication
            Context Class that the authentication performed satisfied.
            The value "0" indicates the End-User authentication did not
            meet the requirements of [ISO29115] level 1. Authentication
            using a long-lived browser cookie, for instance, is one
            example where the use of "level 0" is appropriate.
            Authentications with level 0 SHOULD NOT be used to authorize
            access to any resource of any monetary value.
            (This corresponds to the OpenID 2.0 PAPE [OpenID.PAPE]
            nist_auth_level 0.) An absolute URI or an RFC 6711 [RFC6711]
            registered name SHOULD be used as the acr value;
            registered names MUST NOT be used with a different
            meaning than that which is registered. Parties using
            this claim will need to agree upon the meanings
            of the values used, which may be context-specific.
            The acr value is a case-sensitive string.

        amr
            OPTIONAL. Authentication Methods References. JSON array of
            strings that are identifiers for authentication methods
            used in the authentication. For instance, values might
            indicate that both password and OTP authentication
            methods were used. The definition of particular values
            to be used in the amr Claim is beyond the scope of this
            specification. Parties using this claim will need to
            agree upon the meanings of the values used, which may be
            context-specific. The amr value is an array of case-sensitive
            strings.

        azp
            OPTIONAL. Authorized party - the party to which the
            ID Token was issued. If present, it MUST contain the
            OAuth 2.0 Client ID of this party. This Claim is only
            needed when the ID Token has a single audience value
            and that audience is different from the authorized party.
            It MAY be included even when the authorized party is the
            same as the sole audience. The azp value is a case-sensitive
            string containing a StringOrURI value.

        ID Tokens MAY contain other Claims.
        Any Claims used that are not understood MUST be ignored.

        For additional Claims defined by OpenID Connect specification, see:
            https://openid.net/specs/openid-connect-core-1_0.html#CodeIDToken
            https://openid.net/specs/openid-connect-core-1_0.html#HybridIDToken
            https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims
            https://openid.net/specs/openid-connect-core-1_0.html#SelfIssuedResponse
        """
        payload = {
            "iss": settings.TOKEN_URL,
            "sub": self.client_id,
            "aud": [self.client_id],
            "exp": self.expires_at,
            "iat": self.created_at,
            # TODO: include auth_time
            # TODO: decide if nonce, acr, amr, azp required
        }
        return jwt.encode(payload, self.token, settings.TOKEN_HASH_ALGORITHM)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expires_at = self.created_at + settings.ID_TOKEN_EXPIRATION_TIME
        self.token = self.get_token_jwt()
