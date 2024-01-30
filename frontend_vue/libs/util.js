import config from '~/config'
import Cookies from 'js-cookie'

export const TOKEN_KEY = "token"
// const cookieExpires  = 0.005
// todo: remove test
const cookieExpires  = config.cookieExpires

export const setTokenCookie = (token) => {
  Cookies.set(TOKEN_KEY, token, { expires: cookieExpires || 1 })
}

export const getTokenCookie = () => {
  const token = Cookies.get(TOKEN_KEY)
  if (token)
    return token
  else
    return false
}
