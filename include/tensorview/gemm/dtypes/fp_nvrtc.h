// Copyright 2024 Yan Yan
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
#pragma once
namespace tv {

#ifdef FP_NAN
#undef FP_NAN
#endif
#ifdef FP_INFINITE
#undef FP_INFINITE
#endif
#ifdef FP_ZERO
#undef FP_ZERO
#endif
#ifdef FP_SUBNORMAL
#undef FP_SUBNORMAL
#endif
#ifdef FP_NORMAL
#undef FP_NORMAL
#endif

enum FPClass {
    FP_NAN        = 0,
    FP_INFINITE   = 1,
    FP_ZERO       = 2,
    FP_SUBNORMAL  = 3,
    FP_NORMAL     = 4
};

} // namespace tv
