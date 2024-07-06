// import { Outlet } from 'react-router-dom'
// import React from 'react'

// const Layout = () => {
//   return (
//     <div>
//         <main>
//             <Outlet/>
//         </main>
//     </div>
//   )
// }

// export default Layout

import { Outlet } from "react-router-dom";

import React from 'react'

const Layout = () => {
  return (
    <main>
      <Outlet/>
    </main>
  )
}

export default Layout