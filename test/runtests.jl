#!/usr/bin/env julia

# Copyright 2022 John T. Foster
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import assignment9
using Test
using ImageQualityIndexes
using Images, FileIO

@testset "assignment9.jl" begin
    assignment9.save_png()
    goldfile_path = realpath(dirname(@__FILE__)*"/../images/z_gold.png")
    imgfile_path = realpath(dirname(@__FILE__)*"/../test/z.png")
    img1 = load(goldfile_path)
    img2 = load(imgfile_path)
    @test assess_ssim(img1, img2) >= 0.8
end
