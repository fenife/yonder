import { getTokenCookie } from '~/libs/util'

export default function ({ store, redirect }) {
  // todo: show message: login first
  let token = getTokenCookie()
  if (!token) {
  // if (!store.user) {
    redirect("/signin")
  }
}
