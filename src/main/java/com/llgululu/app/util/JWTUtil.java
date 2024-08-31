package com.llgululu.app.util;



import com.llgululu.app.entity.Userinfo;
import io.jsonwebtoken.*;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class JWTUtil {
    //JWT秘钥
    private static final String AUTHORIZE_TOKEN_SECRET = "llgululu";
    //JWT过期时间，单位毫秒。 1*2*60*60*1000=7200000 2小时
    private static final long AUTHORIZE_TOKEN_EXPIRE = 7200000;

    public static String createJwt(Userinfo user) {
        try {
            SignatureAlgorithm signatureAlgorithm = SignatureAlgorithm.HS256;
            long nowMillis = System.currentTimeMillis();
            long expMillis = nowMillis + AUTHORIZE_TOKEN_EXPIRE;
            Date expDate = new Date(expMillis);
            Date now = new Date(nowMillis);

            Map<String, Object> map = new HashMap<>();
            map.put("uId", user.getuId());
            map.put("uOpenid", user.getuOpenId());

            JwtBuilder builder = Jwts.builder()
                    .setClaims(map)
                    .setIssuer("llgululu")
                    .setIssuedAt(now)
                    .signWith(signatureAlgorithm, AUTHORIZE_TOKEN_SECRET)
                    .setExpiration(expDate);

            return builder.compact();
        } catch (Exception e) {
            // 记录错误日志
            e.printStackTrace();
            // 可能的返回处理或重新抛出异常
            throw new RuntimeException("Error creating JWT", e);
        }
    }

    /**
     * 验证JWT
     */

    public static R<Claims> validateJWT(String token) {
        Claims claims;
        try {
            claims = Jwts.parser()
                    .setSigningKey(AUTHORIZE_TOKEN_SECRET)
                    .parseClaimsJws(token)
                    .getBody();
            return R.ok(claims);
        } catch (ExpiredJwtException e) {
            return R.error(2,"token过期");
        } catch (SignatureException e) {
            return R.error(3,"token校验异常");
        } catch (Exception e) {
            return R.error(4,"token异常");
        }
    }
}